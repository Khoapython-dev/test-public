# Numium Language - Virtual Machine Implementation

Đây là triển khai hoàn chỉnh của Numium Language VM với ba thành phần chính:

## 🏗️ Kiến Trúc

```
numium/
├── vm/
│   ├── compiler/              (Python compiler)
│   │   ├── opcodes.py         (Định nghĩa opcodes)
│   │   ├── lexer.py           (Tokenizer)
│   │   ├── compiler.py        (Biên dịch thành bytecode)
│   │   └── numiac.py          (CLI)
│   │
│   └── runtime/               (C/C++ VM)
│       ├── include/
│       │   └── vm.h           (VM public API)
│       ├── src/
│       │   ├── vm.c           (VM execution engine)
│       │   └── main.c         (Entry point)
│       └── CMakeLists.txt
│
├── examples/
│   └── test.num               (Test program)
│
└── build.sh                   (Build script)
```

## 🔄 Quy Trình Biên Dịch & Chạy

### 1. Biên Dịch Numium → Bytecode (Python)
```bash
python3 vm/compiler/numiac.py examples/test.num -o output.numbc
```

**Input**: Numium source code (plan.txt specification)
**Output**: Binary bytecode (.numbc) + metadata (.meta.json)

### 2. Chạy Bytecode (C/C++ VM)
```bash
./install/bin/numium_vm output.numbc
```

**Input**: Bytecode file
**Output**: Execution result

## 📋 Các Thành Phần

### Python Compiler (vm/compiler/)

- **opcodes.py**: 40+ opcodes cho stack machine
  - Stack: PUSH, POP, DUP
  - Arithmetic: ADD, SUB, MUL, DIV, MOD, NEG
  - Comparison: EQ, NE, LT, LE, GT, GE
  - Logic: AND, OR, NOT
  - Control: JMP, JMP_IF, JMP_IFNOT, CALL, RET
  - I/O: OUTPUT, INPUT
  - Data: MAKE_LIST, MAKE_DICT, LIST_GET, LIST_SET, etc.

- **lexer.py**: Phân tích từ vựng Numium
  - Tokenize keywords, identifiers, literals
  - Handle strings, numbers, hex literals
  - Support all Numium operators

- **compiler.py**: Biên dịch Numium → Bytecode
  - Parser recursive descent
  - Syntax tree to bytecode codegen
  - Variable allocation
  - Function management

- **numiac.py**: Command-line compiler

### C/C++ VM Runtime (vm/runtime/)

- **vm.h**: Public API
  - VM state machine
  - Stack operations
  - Arithmetic/Logic operations
  - I/O operations

- **vm.c**: VM engine (1000+ lines)
  - Bytecode loader
  - Execution loop for all opcodes
  - Value type system (integer, float, string, bool, list, dict)
  - Runtime error handling
  - Memory management

- **main.c**: VM entry point

## 🚀 Hướng Dùng Nhanh

### 1. Build VM
```bash
chmod +x build.sh
./build.sh
```

### 2. Compile example
```bash
python3 vm/compiler/numiac.py examples/test.num -o test.numbc
```

### 3. Run
```bash
./install/bin/numium_vm test.numbc
```

## 📝 Numium Language Features (từ plan.txt)

Hiện tại hỗ trợ:
- ✅ Block system (structural & control flow)
- ✅ Variables (int, float, string, bool, etc.)
- ✅ Arithmetic & comparison operators
- ✅ Control flow (if, for, while, switch, try-catch)
- ✅ Functions (area module, module, local module)
- ✅ Basic I/O (output, input)
- ⏳ Classes & OOP (trong development)
- ⏳ Database structures (trong development)
- ⏳ Library imports (trong development)

## 📦 Bytecode Format

Bytecode file (.numbc):
```
[OPCODE] [ARG_BYTES]* [OPCODE] [ARG_BYTES]* ... [HALT]
```

Metadata file (.meta.json):
```json
{
  "version": 1,
  "constants": [],
  "variables": {},
  "functions": {}
}
```

## 🔧 Tiếp Theo (TODO)

1. **Phase 2 - Object-Oriented Programming**
   - Class implementation
   - Constructor (event)
   - Method calls
   - Inheritance

2. **Phase 3 - Standard Libraries**
   - numium_stdio (input/output)
   - time (delay, getTimeNow)
   - kernel_linker (system, pwd)
   - environment management

3. **Phase 4 - Optimization**
   - Bytecode optimization passes
   - JIT compilation
   - Performance profiling

4. **Phase 5 - Tools**
   - Debugger
   - Profiler
   - Disassembler

## 💡 Kiến Trúc Stack Machine

VM sử dụng stack machine model:
```
[PUSH 5]
[PUSH 3]
[ADD]          → Stack: [8]
[OUTPUT]       → Prints: 8
```

Phù hợp cho:
- Biên dịch dễ dàng
- Execution hiệu quả
- Bytecode compact

## 🐛 Debug Mode

```bash
./install/bin/numium_vm program.numbc --debug
```

Hiển thị:
- PC (Program Counter)
- Stack state
- Variables
- Functions

---

**Version**: 0.1  
**Language Version**: Numium 1.3.2  
**Status**: Alpha - Development in Progress
