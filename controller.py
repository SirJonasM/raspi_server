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

RUN_DURATION = 180
ITERATIONS = 1


def ssh_command(pi_info, command):
    """
    Opens an SSH connection to the Raspberry Pi, executes the given command, and closes the connection.

    Args:
        pi_info (dict): Contains connection information for the Raspberry Pi.
        command (str): The command to execute.

    Returns:
        str: The output of the command if successful.
    Prints:
        Error messages if the command fails.
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


def setup(pi_info):
    """
    Sets up the Raspberry Pi by removing existing files and running the installation script.

    Args:
        pi_info (dict): Contains connection information for the Raspberry Pi.

    Returns:
        bool: True if the setup succeeded, False otherwise.
    """
    command = "cd /home/jonas/git-repos/raspi_server && " "rm -f *.csv"
    ssh_command(pi_info, command)

    print("Running install_full.sh...")
    command = "cd /home/jonas/git-repos/raspi_server && " "./install_full.sh"
    out = ssh_command(pi_info, command)

    # Check if the installation succeeded
    if "Installation completed" in out:
        print("Installation succeeded.")
        return True

    print("Installation failed.")
    return False


def start_server(pi_info):
    """
    Starts the Flask server on the Raspberry Pi in the background.

    Args:
        pi_info (dict): Contains connection information for the Raspberry Pi.

    Returns:
        str: The process ID (PID) of the server process.
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
    Starts the client process on the Raspberry Pi in the background.

    Args:
        pi_info (dict): Contains connection information for the Raspberry Pi.
        server_ip (str): The IP address of the server.

    Returns:
        str: The process ID (PID) of the client process.
    """
    command = (
        f"cd /home/jonas/git-repos/raspi_server && "
        f"nohup .venv/bin/python client.py {server_ip} > client.log 2>&1 & "
        f"echo $! && exit 0"
    )
    pid = ssh_command(pi_info, command)
    return pid


def stop_process(pi_info, pid):
    """
    Stops a process on the Raspberry Pi by killing its PID.

    Args:
        pi_info (dict): Contains connection information for the Raspberry Pi.
        pid (str): The process ID (PID) to kill.
    """
    if not pid:
        return
    command = f"kill {pid} || true"
    ssh_command(pi_info, command)


def download_file(pi_info, remote_path, local_path):
    """
    Downloads a file from the Raspberry Pi to the local machine.

    Args:
        pi_info (dict): Contains connection information for the Raspberry Pi.
        remote_path (str): The path to the file on the Raspberry Pi.
        local_path (str): The path where the file will be saved locally.
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
    """
    Combines two CSV files into a single file and saves it in the output directory.

    Args:
        file1 (str): Path to the first CSV file.
        file2 (str): Path to the second CSV file.
        output_file (str): Name of the output CSV file.

    Side Effects:
        - Saves the combined CSV file in the `output` directory.
        - Removes the original files after combining.
    """
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    combined_df = pd.concat([df1, df2], ignore_index=True)

    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_file)
    combined_df.to_csv(output_path, index=False, header=True)
    print(f"Combined {file1} and {file2} into {output_file}")

    os.remove(file1)
    os.remove(file2)


def run_benchmark(pi_a, pi_b):
    """
    Executes a single benchmark iteration by running the server on one Raspberry Pi
    and the client on the other for a fixed duration.

    Args:
        pi_a (dict): Information for the first Raspberry Pi (acts as client/server).
        pi_b (dict): Information for the second Raspberry Pi (acts as server/client).
    """
    pid_server_b = start_server(pi_b)

    pid_client_a = start_client(pi_a, pi_b["url"])

    time.sleep(RUN_DURATION)

    stop_process(pi_b, pid_server_b)
    stop_process(pi_a, pid_client_a)


def get_results():
    """
    Handles the final steps after benchmarks, including:
    - Downloading timing and performance CSV files from both Raspberry Pis.
    - Combining the CSV files into single consolidated files.
    - Saving the consolidated files locally.
    """
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


def main():
    """
    Main function to set up Raspberry Pis, run multiple benchmark iterations,
    and process the results.

    - Sets up the environment on both Raspberry Pis.
    - Executes `ITERATIONS` benchmark iterations, swapping server/client roles.
    - Consolidates results into combined CSV files.
    """
    setup(PI_A)
    setup(PI_B)

    for i in range(ITERATIONS):
        print(f"[INFO] Iteration {i}")
        run_benchmark(PI_A, PI_B)
        print("[INFO] Swapping roles")
        run_benchmark(PI_B, PI_A)

    get_results()


if __name__ == "__main__":
    """
    Entry point of the script. Executes the main function to:
    - Set up Raspberry Pis.
    - Run benchmarks.
    - Consolidate results.
    """
    main()
