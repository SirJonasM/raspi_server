import os
import subprocess

# Directory where all the Makefiles are stored
MAKEFILES_DIR = "./Makefiles"

def run_makefile(makefile_path):
    """
    Runs a given Makefile using the `make` command.
    """
    try:
        print(f"Building {makefile_path}...")
        subprocess.run(
            ["make", "-f", makefile_path], 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print(f"Successfully built {makefile_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error building {makefile_path}:")
        print(e.stderr.decode())

def build_all_makefiles():
    """
    Finds and runs all Makefiles in the MAKEFILES_DIR.
    """
    # Ensure the directory exists
    if not os.path.exists(MAKEFILES_DIR):
        print(f"Directory {MAKEFILES_DIR} does not exist.")
        return

    # Iterate through all Makefiles in the directory
    for filename in os.listdir(MAKEFILES_DIR):
        if filename.startswith("Makefile."):  # Ensure it's a Makefile
            makefile_path = os.path.join(MAKEFILES_DIR, filename)
            run_makefile(makefile_path)

if __name__ == "__main__":
    build_all_makefiles()

