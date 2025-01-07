import os

# Paths to the directories containing the libraries
BASE_DIR = "./PQClean"
KEM_DIR = os.path.join(BASE_DIR, "crypto_kem")
SIGN_DIR = os.path.join(BASE_DIR, "crypto_sign")

# Template for the Makefile
MAKEFILE_TEMPLATE = """CC = gcc
CFLAGS = -Wall -Wextra -O3 -fPIC -I./PQClean/common
TARGET = ./build/{type}/lib{target}
COMMON_SRCS = ./PQClean/common/*.c

IMPL_SRCS = ./PQClean/{type}/{library}/clean/*.c

all: $(TARGET)

$(TARGET): $(IMPL_SRCS) $(COMMON_SRCS)
\t$(CC) -shared $(CFLAGS) -o $@ $(IMPL_SRCS) $(COMMON_SRCS)

clean:
\trm -f $(TARGET)
"""

# Output directory for the Makefiles
OUTPUT_DIR = "./Makefiles"

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_libraries(base_dir):
    """
    Traverse the base directory to find all library paths under `clean`.
    Returns a list of (type, library_name) tuples.
    """
    libraries = []
    for root, dirs, _ in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name == "clean":
                # Extract type (e.g., crypto_kem or crypto_sign) and library name
                rel_path = os.path.relpath(root, BASE_DIR)
                type_name = rel_path.split(os.sep)[0]
                library_name = os.path.basename(root)
                libraries.append((type_name, library_name))
    return libraries

def create_makefile(type_name, library_name):
    """
    Generate a Makefile for the given library using the template.
    """
    target_name = f"{library_name}.so"
    makefile_content = MAKEFILE_TEMPLATE.format(
        target=target_name,
        type=type_name,
        library=library_name
    )
    
    # Save the Makefile to the output directory
    makefile_path = os.path.join(OUTPUT_DIR, f"Makefile.{library_name}")
    with open(makefile_path, "w") as makefile:
        makefile.write(makefile_content)
    print(f"Makefile created for {type_name}/{library_name}: {makefile_path}")

# Main script logic
def main():
    # Collect libraries from KEM and SIGN directories
    kem_libraries = find_libraries(KEM_DIR)
    sign_libraries = find_libraries(SIGN_DIR)
    for type_name, library_name in sign_libraries:
        api_path = SIGN_DIR + os.sep + library_name + os.sep + "clean" + os.sep + "api.h"
        with open(api_path, "r") as api_file:
            api_file


    all_libraries = kem_libraries + sign_libraries
    
    # Generate Makefiles for each library
    for type_name, library_name in all_libraries:
        create_makefile(type_name, library_name)

if __name__ == "__main__":
    main()

