#!/bin/bash

# Set the output directory for shared libraries
OUTPUT_DIR="../build/crypto_kem"

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Define build configurations
declare -A builds=(
  ["kyber512"]="libkyber512rust.so"
  ["kyber1024"]="libkyber1024rust.so"
  ["std"]="libkyber768rust.so"
)

# Function to build and copy .so file
build_and_copy() {
  local features=$1
  local output_file=$2

  echo "Building with features: $features"
  
  # Build the project with the specified features
  cargo build --release --features "$features"

  # Find the generated .so file
  SO_FILE=$(find target/release -name "lib*.so" | head -n 1)

  if [[ -f "$SO_FILE" ]]; then
    echo "Copying $SO_FILE to $OUTPUT_DIR/$output_file"
    cp "$SO_FILE" "$OUTPUT_DIR/$output_file"
  else
    echo "Error: Shared library not found for features: $features"
    exit 1
  fi
}

# Build and copy for each configuration
for features in "${!builds[@]}"; do
  build_and_copy "$features" "${builds[$features]}"
done

echo "All builds completed successfully!"

