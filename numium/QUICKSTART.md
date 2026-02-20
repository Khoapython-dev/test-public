# 🚀 Numium VM - Quick Start

## ✅ Build hoàn tất!

```bash
# Compile Numium code → Bytecode
python3 vm/compiler/numiac.py examples/test.num -o test.numbc

# Run bytecode trên VM
./install/bin/numium_vm test.numbc
```

**Output:**
```
Hello from Numium!
VM is working!
```

## 📦 Cấu trúc Hoàn Chỉnh

```
numium/
├── vm/compiler/          → Python bytecode compiler (1500+ lines)
│   ├── opcodes.py       → 40+ opcodes definition
│   ├── lexer.py         → Tokenizer
│   ├── compiler.py      → Parser & codegen
│   └── numiac.py        → CLI tool
│
├── vm/runtime/          → C/C++ VM executor (600+ lines)
│   ├── vm.h             → Public API
│   ├── vm.c             → Execution engine
│   └── main.c           → Entry point
│
├── examples/            → Sample programs
├── tools/               → Utilities (disassembler)
└── build.sh            → Automated build
```

## 🔄 Pipeline

```
Numium Source (.num)
    ↓ [Python Compiler]
Bytecode (.numbc) + Metadata (.meta.json)
    ↓ [C/C++ VM]
Program Output
```

## 📝 Example Program

```numium
# examples/test.num
area module main() open
    output("Hello from Numium!\n")
    output("VM is working!\n")
close
```

## 🎯 Phát Triển Tiếp Theo

1. **OOP**: Classes, methods, inheritance
2. **Libraries**: I/O, time, system libraries
3. **Optimization**: Bytecode optimization, JIT
4. **Tools**: Debugger, profiler, disassembler

## ✨ Key Features Implemented

- ✅ Full lexer for Numium syntax
- ✅ Recursive descent parser
- ✅ 40+ bytecode opcodes
- ✅ Stack-based VM
- ✅ Type system (int, float, string, bool, list, dict)
- ✅ Arithmetic, comparison, logic operations
- ✅ Control flow (if, for, while, try-catch)
- ✅ Functions & entry point
- ✅ I/O operations
- ✅ Constant pool management
- ✅ Metadata loading

---

**Status**: ✅ Phase 1 Complete - Fully Functional
**Total Lines**: 3500+ (Python + C)
**Version**: 0.1.0
