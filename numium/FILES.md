# Numium VM Project Files

## Documentation
- plan.txt                  - Official Numium 1.3.2 specification
- README.md                - User guide and quick start
- DEVELOPMENT.md           - Developer guide and contribution info
- Makefile                 - Build shortcuts

## Compiler (Python)
- vm/compiler/opcodes.py           - Bytecode instruction definitions
- vm/compiler/lexer.py             - Tokenizer for Numium syntax
- vm/compiler/compiler.py          - Parser and bytecode generator
- vm/compiler/numiac.py            - CLI tool for compilation
- vm/compiler/__init__.py          - Package initialization

## Runtime (C/C++)
- vm/runtime/include/vm.h          - VM public API
- vm/runtime/src/vm.c              - VM execution engine (1000+ lines)
- vm/runtime/src/main.c            - VM entry point
- vm/runtime/CMakeLists.txt        - C runtime build config
- vm/CMakeLists.txt                - Main build config

## Tools
- tools/disasm.py         - Bytecode disassembler

## Examples
- examples/test.num       - Test Numium program

## Build System
- build.sh               - Automated build script
- install.sh            - Installation script with dependency check
- setup.py              - Python package setup
- .gitignore            - Git ignore patterns

## Architecture Overview

```
┌─────────────────────────────────────────┐
│           Numium Source Code            │
│              (.num file)                │
└──────────────────┬──────────────────────┘
                   │
                   ↓
         ┌─────────────────────┐
         │ PYTHON COMPILER     │
         │  (Lexer→Parser)     │
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │   BYTECODE OUTPUT   │
         │  .numbc + .meta.json│
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │   C/C++ VM RUNTIME  │
         │  (Execution Engine) │
         └──────────┬──────────┘
                    │
                    ↓
         ┌─────────────────────┐
         │  PROGRAM OUTPUT     │
         │  (Console/Files)    │
         └─────────────────────┘
```

## File Statistics

- Python Compiler: ~1500 lines (3 files)
- C Runtime: ~1000+ lines (3 files)  
- Documentation: ~500 lines (3 files)
- Total: ~3500+ lines of code & docs

## Next Phase TODO

1. **Object-Oriented Programming**
   - Class definitions
   - Methods and constructors
   - Inheritance

2. **Standard Libraries**
   - I/O library (stdio)
   - Time library
   - System library (kernel_linker)

3. **Advanced Optimizations**
   - Constant folding
   - Dead code elimination
   - Bytecode optimization

4. **Runtime Features**
   - Exception handling
   - Memory management
   - Profiling support
