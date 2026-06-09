#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_DIR="$REPO_ROOT/.venv"

# Create venv at repo root if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

echo "Installing requirements..."
pip install --upgrade pip -q
pip install -r "$SCRIPT_DIR/requirements.txt"

# Generate gRPC stubs from the proto file
echo "Generating gRPC stubs..."
cd "$SCRIPT_DIR/networking"
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. motor_control.proto

echo "Setup complete. Activate the venv with: source $VENV_DIR/bin/activate"
