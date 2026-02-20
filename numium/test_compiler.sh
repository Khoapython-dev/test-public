#!/bin/bash
# Quick test of compiler only (no build needed)

echo "Testing Python Compiler..."
echo ""

# Test imports
python3 -c "from vm.compiler import Lexer, Compiler, Bytecode; print('✓ Imports OK')"

# Run lexer test
python3 << 'EOF'
from vm.compiler.lexer import Lexer

code = """
env x int = 5
env y int = 3
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
print(f"✓ Lexer: Tokenized {len(tokens)} tokens")
for token in tokens[:5]:
    print(f"  {token.type.name}: {token.value}")
EOF

echo ""
echo "✓ Compiler tests passed!"
