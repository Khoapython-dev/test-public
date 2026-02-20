#!/bin/bash
# Installation script for Numium VM & Compiler

set -e

echo "=========================================="
echo "Numium VM & Compiler Installation"
echo "=========================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION detected"

# Check CMake
if ! command -v cmake &> /dev/null; then
    echo "✗ CMake not found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y cmake build-essential
    elif command -v brew &> /dev/null; then
        brew install cmake
    else
        echo "Please install CMake manually"
        exit 1
    fi
fi

CMAKE_VERSION=$(cmake --version 2>&1 | head -n1 | awk '{print $3}')
echo "✓ CMake $CMAKE_VERSION detected"

# Check GCC/Clang
if ! command -v gcc &> /dev/null && ! command -v clang &> /dev/null; then
    echo "✗ No C compiler found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y build-essential
    elif command -v brew &> /dev/null; then
        brew install gcc
    fi
fi

echo "✓ C compiler detected"

echo ""
echo "Building VM runtime..."
./build.sh

echo ""
echo "Installing Python compiler..."
chmod +x vm/compiler/numiac.py
chmod +x tools/disasm.py
chmod +x build.sh

echo ""
echo "=========================================="
echo "✓ Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Try compiling an example:"
echo "   python3 vm/compiler/numiac.py examples/test.num"
echo ""
echo "2. Run the compiled bytecode:"
echo "   ./install/bin/numium_vm examples/test.numbc"
echo ""
echo "3. Disassemble bytecode:"
echo "   python3 tools/disasm.py examples/test.numbc --metadata"
echo ""
