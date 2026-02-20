#!/usr/bin/env python3
"""
Numium Compiler CLI
Biên dịch file Numium thành bytecode
"""

import sys
import argparse
from compiler import compile_file

def main():
    parser = argparse.ArgumentParser(
        description='Numium Language Compiler',
        epilog='Example: numiac hello.num -o hello.numbc'
    )
    
    parser.add_argument('input', help='Source file (.num)')
    parser.add_argument('-o', '--output', help='Output bytecode file (.numbc)', default=None)
    parser.add_argument('--debug', action='store_true', help='Print debug information')
    parser.add_argument('--version', action='version', version='Numium Compiler v0.1')
    
    args = parser.parse_args()
    
    # Determine output filename
    if args.output is None:
        output_file = args.input.replace('.num', '.numbc')
    else:
        output_file = args.output
    
    try:
        print(f"Compiling {args.input}...")
        bytecode = compile_file(args.input, output_file)
        
        if args.debug:
            print("\n=== Bytecode Metadata ===")
            print(f"Bytecode size: {len(bytecode.code)} bytes")
            print(f"Constants: {len(bytecode.constants)}")
            print(f"Variables: {dict(bytecode.variables)}")
            print(f"Functions: {dict(bytecode.functions)}")
        
        print(f"✓ Successfully compiled to {output_file}")
        return 0
        
    except Exception as e:
        print(f"✗ Compilation failed: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
