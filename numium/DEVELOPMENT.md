# Numium Language VM - Development Guide

## 📚 Cấu trúc Dự Án

```
numium/
├── vm/                          # Core VM implementation
│   ├── compiler/                # Python bytecode compiler
│   │   ├── __init__.py
│   │   ├── opcodes.py          # Bytecode instruction definitions
│   │   ├── lexer.py            # Tokenization
│   │   ├── compiler.py         # Parser & codegen
│   │   └── numiac.py           # CLI tool
│   │
│   ├── runtime/                 # C/C++ execution engine
│   │   ├── include/
│   │   │   └── vm.h            # VM public API
│   │   ├── src/
│   │   │   ├── vm.c            # VM core
│   │   │   └── main.c          # Entry point
│   │   └── CMakeLists.txt
│   │
│   ├── __init__.py
│   └── CMakeLists.txt
│
├── examples/                    # Example programs
│   └── test.num
│
├── plan.txt                     # Specification for Numium language
├── README.md                    # User documentation
├── DEVELOPMENT.md              # This file
├── setup.py                    # Python package setup
├── build.sh                    # Build script
└── .gitignore
```

## 🔄 Development Workflow

### 1. **Compiler Development** (Python)

File: `vm/compiler/`

Add new features:
1. Add tokens to `lexer.py` (TokenType enum)
2. Add opcodes to `opcodes.py` (Opcode class)
3. Implement parsing in `compiler.py` (compile_xxx methods)
4. Test with examples/test.num

Example - Add IF statement support:
```python
# lexer.py - Already done
# opcodes.py - Already done (JMP, JMP_IF, JMP_IFNOT)

# compiler.py - Modify compile_if()
def compile_if(self):
    self.expect(TokenType.KEYWORD)  # 'if'
    self.compile_condition()
    self.expect(TokenType.KEYWORD)  # 'do'
    
    jmp_if_false = len(self.bytecode.code)
    self.bytecode.emit(Opcode.JMP_IFNOT, 0)  # Placeholder
    
    self.skip_newlines()
    self.compile_block()
    
    # Patch jump address
    self.bytecode.code[jmp_if_false + 1] = len(self.bytecode.code) & 0xFF
    
    self.expect(TokenType.KEYWORD)  # 'end'
```

### 2. **Runtime Development** (C/C++)

File: `vm/runtime/`

Add new opcodes:
1. Add case in `vm_run()` switch statement
2. Implement helper functions if needed
3. Add tests

Example - Add NEW opcode:
```c
// vm.h - Define opcode
#define OP_NEW_OPCODE 0xAB

// vm.c - Implement in vm_run()
case OP_NEW_OPCODE: {
    // Implementation
    break;
}

// Rebuild
./build.sh
```

### 3. **Testing**

1. Create test program (examples/test.num)
2. Compile: `python3 vm/compiler/numiac.py examples/test.num -o test.numbc`
3. Run: `./install/bin/numium_vm test.numbc`
4. Debug: `./install/bin/numium_vm test.numbc --debug`

## 🔧 Build Process

```bash
# Clean
./build.sh clean

# Build
./build.sh

# Artifacts
build/          - CMake build directory
install/        - Final binaries
  └── bin/
      └── numium_vm
```

## 📋 Compiler Phases

```
Input (test.num)
    ↓
[LEXER] → Tokens
    ↓
[PARSER] → AST
    ↓
[CODEGEN] → Bytecode + Metadata
    ↓
Output (.numbc, .meta.json)
```

## 🎯 Implementation Checklist

### Phase 1: Core VM ✅ (Done)
- [x] Lexer for Numium
- [x] Parser (recursive descent)
- [x] Bytecode codegen
- [x] Stack-based VM
- [x] Integer/Float/String types
- [x] Arithmetic operations
- [x] Comparison operations
- [x] Logic operations
- [x] Basic control flow (if, while, for)
- [x] Functions
- [x] I/O (output, input)
- [x] Error handling

### Phase 2: OOP Features 🔄 (TODO)
- [ ] Class definitions
- [ ] Constructor (event)
- [ ] Instance methods
- [ ] Visibility (private/public)
- [ ] Inheritance
- [ ] Method polymorphism

### Phase 3: Standard Libraries 📚 (TODO)
- [ ] numium_stdio
- [ ] time library
- [ ] kernel_linker
- [ ] environment library
- [ ] List/Dict operations

### Phase 4: Advanced Features 🚀 (TODO)
- [ ] Exception handling (try-catch)
- [ ] Closures
- [ ] Generator support
- [ ] Decorators
- [ ] Type annotations

### Phase 5: Optimization ⚡ (TODO)
- [ ] Constant folding
- [ ] Dead code elimination
- [ ] Bytecode optimization
- [ ] JIT compilation
- [ ] Profiling support

## 🐛 Common Issues & Solutions

### Issue: "Unterminated string" error
**Solution**: Check closing quotes in lexer.read_string()

### Issue: Stack overflow during execution
**Solution**: Increase STACK_SIZE in vm.h or check for infinite recursion

### Issue: Undefined reference errors during build
**Solution**: 
```bash
rm -rf build install
./build.sh
```

### Issue: Bytecode size too large
**Solution**: Implement constant pooling optimization

## 📖 References

- **Numium Language Spec**: [plan.txt](plan.txt)
- **VM Architecture**: Stack-based, Bytecode interpreter
- **Instruction Set**: 40+ opcodes (see opcodes.py)

## 🚀 Quick Start for Contributors

1. Clone and build:
```bash
./build.sh
```

2. Create test file:
```bash
cat > examples/mytest.num << 'EOF'
area module main() open
    output("Hello from Numium!\n")
close
EOF
```

3. Compile:
```bash
python3 vm/compiler/numiac.py examples/mytest.num
```

4. Run:
```bash
./install/bin/numium_vm examples/mytest.numbc
```

5. Debug:
```bash
./install/bin/numium_vm examples/mytest.numbc --debug
```

## 💡 Tips

- Keep opcodes simple for efficient compilation
- Test each feature in isolation
- Use --debug flag for VM troubleshooting
- Profile bytecode size with `wc -c <file>.numbc`
- Study the compiler phases carefully before extending

---

**Status**: Active Development  
**Language**: Numium 1.3.2  
**VM Version**: 0.1.0
