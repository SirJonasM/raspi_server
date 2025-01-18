import time
import paramiko
import pandas as pd
import os

# -----------------------------------------
# ADJUST THESE TO MATCH YOUR ENVIRONMENT
# -----------------------------------------
PI_A = {
    "hostname": "raspi3",
    "username": "jonas",
    "key_filename": "/home/jonas/.ssh/id_ed25519",
    "url": "192.168.178.98",
}

PI_B = {
    "hostname": "raspi",
    "username": "jonas",
    "key_filename": "/home/jonas/.ssh/id_ed25519",
    "url": "192.168.178.87",
}

SERVER_SCRIPT = "/home/jonas/git-repos/raspi_server/server.py"
CLIENT_SCRIPT = "/home/jonas/git-repos/raspi_server/client.py"

RUN_DURATION = 300
ITERATIONS = 0


def ssh_command(pi_info, command):
    """
    Opens an SSH connection to the pi, runs the command, and closes the connection.
    Returns the output if needed (but here we won't).
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=pi_info["hostname"],
        username=pi_info["username"],
        key_filename=pi_info.get("key_filename"),
        password=pi_info.get("password"),
    )

    stdin, stdout, stderr = ssh.exec_command(command)
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    ssh.close()

    if err:
        print(f"[ERROR - {pi_info['hostname']}] {err}")
    if out:
        print(f"[OUTPUT - {pi_info['hostname']}] {out}")
    return out


def start_server(pi_info):
    """
    Start the Flask server in the background on the remote Pi.
    We'll redirect output to server.log for debugging.
    'nohup' + '&' ensures it keeps running in the background after SSH session ends.
    """
    command = (
        "cd /home/jonas/git-repos/raspi_server && "
        "nohup .venv/bin/python server.py > server.log 2>&1 & "
        "echo $! && exit 0"
    )
    pid = ssh_command(pi_info, command)
    print(f"[INFO] Server started on {pi_info['hostname']} with PID {pid}")
    return pid


def start_client(pi_info, server_ip):
    """
    Start the client in the background, passing in the server IP as argument
    (assuming client.py accepts e.g. `python client.py 192.168.1.10`).
    We'll also redirect output to client.log.
    """
    command = (
        f"cd /home/jonas/git-repos/raspi_server && "
        f"nohup .venv/bin/python client.py {server_ip} > client.log 2>&1 & "
        f"echo $! && exit 0"
    )
    pid = ssh_command(pi_info, command)
    print(f"[INFO] Client started on {pi_info['hostname']} with PID {pid}")
    return pid


def stop_process(pi_info, pid):
    """
    Kills a process (PID) on the remote Pi.
    """
    if not pid:
        return
    command = f"kill {pid} || true"
    ssh_command(pi_info, command)
    print(f"[INFO] Killed process {pid} on {pi_info['hostname']}")


def download_file(pi_info, remote_path, local_path):
    """
    Downloads a file from the remote Raspberry Pi to the local machine.

    Parameters:
        pi_info (dict): Contains connection info for the Raspberry Pi.
        remote_path (str): The full path to the file on the remote Pi.
        local_path (str): The local path where the file will be saved.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=pi_info["hostname"],
        username=pi_info["username"],
        key_filename=pi_info["key_filename"],
    )
    try:
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        print(
            f"[INFO] Downloaded {remote_path} from {pi_info['hostname']} to {local_path}"
        )
        sftp.close()
    except Exception as e:
        print(
            f"[ERROR] Failed to download {remote_path} from {pi_info['hostname']}: {e}"
        )
    finally:
        ssh.close()


def combine_csv(file1, file2, output_file):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    print(df1)
    print(df2)
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Write the combined dataframe to the output file without adding a header
    combined_df.to_csv(output_file, index=False, header=False)
    print(f"Combined {file1} and {file2} into {output_file}")

    os.remove(file1)
    os.remove(file2)
    print(f"Deleted {file1} and {file2}")


def main():
    for i in range(ITERATIONS):
        # ----------------------
        # 1) Pi A → SERVER
        #    Pi B → CLIENT
        # ----------------------
        print("[INFO] Starting Pi A as server, Pi B as client")

        pid_server_b = start_server(PI_B)

        pid_client_a = start_client(PI_A, PI_B["url"])

        # 2.3) Let them run for RUN_DURATION
        time.sleep(RUN_DURATION)

        # 2.4) Stop them
        stop_process(PI_B, pid_server_b)
        stop_process(PI_A, pid_client_a)

        # ----------------------
        # 2) Swap roles:
        #    Pi B → SERVER
        #    Pi A → CLIENT
        # ----------------------
        print("[INFO] Swapping roles: Pi B as server, Pi A as client")

        # 1.1) Start server on Pi A
        print("starting Server!")
        pid_server_a = start_server(PI_A)
        print("starting Client!")
        # 1.2) Start client on Pi B (target = Pi A's IP)
        pid_client_b = start_client(PI_B, PI_A["url"])

        # 1.3) Let them run for RUN_DURATION
        time.sleep(RUN_DURATION)

        # 1.4) Stop them
        stop_process(PI_A, pid_server_a)
        stop_process(PI_B, pid_client_b)

    download_file(
        PI_A,
        "/home/jonas/git-repos/raspi_server/client_timings.csv",
        "./client_timings_pi3.csv",
    )
    download_file(
        PI_B,
        "/home/jonas/git-repos/raspi_server/client_timings.csv",
        "./client_timings_pi2W.csv",
    )
    combine_csv(
        "client_timings_pi3.csv",
        "client_timings_pi2W.csv",
        "combined_client_timings.csv",
    )
    download_file(
        PI_B,
        "/home/jonas/git-repos/raspi_server/server_timings.csv",
        "./server_timings_pi2W.csv",
    )
    download_file(
        PI_A,
        "/home/jonas/git-repos/raspi_server/server_timings.csv",
        "./server_timings_pi3.csv",
    )
    combine_csv(
        "server_timings_pi3.csv",
        "server_timings_pi2W.csv",
        "combined_server_timings.csv",
    )
    download_file(
        PI_A,
        "/home/jonas/git-repos/raspi_server/key_generation_times.csv",
        "./key_generation_times_pi3.csv",
    )
    download_file(
        PI_B,
        "/home/jonas/git-repos/raspi_server/key_generation_times.csv",
        "./key_generation_times_pi2W.csv",
    )
    combine_csv(
        "key_generation_times_pi3.csv",
        "key_generation_times_pi2W.csv",
        "combined_key_generation_times.csv",
    )


if __name__ == "__main__":
    main()
