"""
Numium Virtual Machine - Bytecode Disassembler
Công cụ để xem bytecode ở dạng readable
"""

import struct
import json
import sys
from vm.compiler.opcodes import OPCODE_NAMES

class Disassembler:
    def __init__(self, bytecode_file):
        self.bytecode_file = bytecode_file
        self.metadata_file = bytecode_file.replace('.numbc', '.meta.json')
        self.code = []
        self.metadata = {}
    
    def load(self):
        """Load bytecode and metadata"""
        with open(self.bytecode_file, 'rb') as f:
            self.code = list(f.read())
        
        try:
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        except FileNotFoundError:
            pass
    
    def disassemble(self):
        """Disassemble bytecode to assembly-like format"""
        pc = 0
        while pc < len(self.code):
            opcode = self.code[pc]
            opname = OPCODE_NAMES.get(opcode, f"UNKNOWN({opcode:02X})")
            
            # Check if opcode has argument
            if opcode in (0x01, 0x40, 0x41, 0x42, 0x50, 0x51, 0x52, 0x53):
                if pc + 4 < len(self.code):
                    arg = (self.code[pc+1] | 
                           (self.code[pc+2] << 8) |
                           (self.code[pc+3] << 16) |
                           (self.code[pc+4] << 24))
                    print(f"0x{pc:04X}: {opname:12} 0x{arg:08X}")
                    pc += 5
                else:
                    print(f"0x{pc:04X}: {opname}")
                    pc += 1
            else:
                print(f"0x{pc:04X}: {opname}")
                pc += 1
    
    def print_metadata(self):
        """Print metadata information"""
        if not self.metadata:
            print("No metadata found")
            return
        
        print("\n=== Constants ===")
        for i, const in enumerate(self.metadata.get('constants', [])):
            print(f"{i}: {const}")
        
        print("\n=== Variables ===")
        for name, idx in self.metadata.get('variables', {}).items():
            print(f"{idx}: {name}")
        
        print("\n=== Functions ===")
        for name, addr in self.metadata.get('functions', {}).items():
            print(f"0x{addr:04X}: {name}")
    
    def run(self, show_metadata=False):
        print(f"=== Disassembly: {self.bytecode_file} ===\n")
        self.disassemble()
        if show_metadata:
            self.print_metadata()

def main():
    if len(sys.argv) < 2:
        print("Usage: disasm.py <bytecode_file> [--metadata]")
        sys.exit(1)
    
    bytecode_file = sys.argv[1]
    show_metadata = '--metadata' in sys.argv
    
    disasm = Disassembler(bytecode_file)
    disasm.load()
    disasm.run(show_metadata)

if __name__ == '__main__':
    main()
