#!/bin/bash
# Build script for Numium VM

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
INSTALL_DIR="$SCRIPT_DIR/install"

echo "=========================================="
echo "Numium VM Build System"
echo "=========================================="

# Clean option
if [ "$1" == "clean" ]; then
    echo "Cleaning build artifacts..."
    rm -rf "$BUILD_DIR" "$INSTALL_DIR"
    echo "Clean complete"
    exit 0
fi

# Create build directory
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

echo ""
echo "Configuring CMake..."
cmake -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" "$SCRIPT_DIR"

echo ""
echo "Building C/C++ runtime..."
make -j$(nproc)

echo ""
echo "Installing..."
make install

echo ""
echo "=========================================="
echo "Build complete!"
echo "=========================================="
echo ""
echo "VM executable: $INSTALL_DIR/bin/numium_vm"
echo "Python compiler: $SCRIPT_DIR/vm/compiler/numiac.py"
echo ""
echo "Usage:"
echo "  1. Compile Numium code:"
echo "     python3 $SCRIPT_DIR/vm/compiler/numiac.py program.num -o program.numbc"
echo "  2. Run bytecode:"
echo "     $INSTALL_DIR/bin/numium_vm program.numbc"
echo ""
