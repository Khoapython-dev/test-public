"""
Numium Compiler - Convert Numium code to bytecode
Biên dịch mã Numium thành bytecode
"""

import struct
import json
from typing import List, Dict, Any, Optional
from lexer import Lexer, Token, TokenType
from opcodes import Opcode, OPCODE_NAMES

class Bytecode:
    """Bytecode output"""
    def __init__(self):
        self.code: List[int] = []
        self.constants: List[Any] = []
        self.variables: Dict[str, int] = {}
        self.functions: Dict[str, int] = {}
        self.metadata: Dict[str, Any] = {
            'version': 1,
            'constants': self.constants,
            'variables': self.variables,
            'functions': self.functions,
        }
    
    def emit(self, opcode: int, arg: int = 0):
        """Emit an opcode instruction"""
        self.code.append(opcode)
        # Always emit argument for opcodes that take arguments
        if opcode in (Opcode.PUSH, Opcode.LOAD_VAR, Opcode.STORE_VAR, Opcode.INIT_VAR, 
                      Opcode.JMP, Opcode.JMP_IF, Opcode.JMP_IFNOT, Opcode.CALL):
            # Emit argument as 4 bytes (little-endian)
            self.code.extend([arg & 0xFF, (arg >> 8) & 0xFF, (arg >> 16) & 0xFF, (arg >> 24) & 0xFF])
    
    def add_constant(self, value: Any) -> int:
        """Add a constant and return its index"""
        self.constants.append(value)
        return len(self.constants) - 1
    
    def add_variable(self, name: str) -> int:
        """Add a variable and return its index"""
        if name not in self.variables:
            self.variables[name] = len(self.variables)
        return self.variables[name]
    
    def to_bytes(self) -> bytes:
        """Convert to bytecode bytes"""
        return bytes(self.code)
    
    def to_file(self, filename: str):
        """Write bytecode to file"""
        with open(filename, 'wb') as f:
            f.write(self.to_bytes())
        
        # Also write metadata as JSON
        metadata_file = filename.replace('.numbc', '.meta.json')
        with open(metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

class Compiler:
    def __init__(self, source: str):
        self.source = source
        self.lexer = Lexer(source)
        self.tokens = self.lexer.tokenize()
        self.position = 0
        self.bytecode = Bytecode()
    
    def error(self, message: str):
        if self.position < len(self.tokens):
            token = self.tokens[self.position]
            raise SyntaxError(f"Compiler error at line {token.line}, column {token.column}: {message}")
        raise SyntaxError(f"Compiler error: {message}")
    
    def peek(self, offset: int = 0) -> Optional[Token]:
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Optional[Token]:
        token = self.peek()
        if token:
            self.position += 1
        return token
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.peek()
        if not token or token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type if token else 'EOF'}")
        return self.advance()
    
    def skip_newlines(self):
        while self.peek() and self.peek().type == TokenType.NEWLINE:
            self.advance()
    
    def compile(self) -> Bytecode:
        """Main compilation entry point"""
        try:
            self.skip_newlines()
            
            # Parse top-level constructs
            while self.peek() and self.peek().type != TokenType.EOF:
                self.skip_newlines()
                
                token = self.peek()
                if not token or token.type == TokenType.EOF:
                    break
                
                if token.type == TokenType.KEYWORD:
                    if token.value == 'import':
                        self.compile_import()
                    elif token.value == 'INIT':
                        self.compile_init()
                    elif token.value == 'env':
                        self.compile_env_declaration()
                    elif token.value == 'area':
                        self.compile_area()
                    elif token.value == 'module':
                        self.compile_module()
                    elif token.value == 'class':
                        self.compile_class()
                    else:
                        self.error(f"Unexpected keyword at top level: {token.value}")
                else:
                    self.error(f"Unexpected token at top level: {token.value}")
                
                self.skip_newlines()
            
            # Emit HALT at end
            self.bytecode.emit(Opcode.HALT)
            
        except Exception as e:
            print(f"Compilation failed: {e}")
            raise
        
        return self.bytecode
    
    def compile_import(self):
        """Compile: import <library_name>"""
        self.expect(TokenType.KEYWORD)  # 'import'
        lib_name = self.expect(TokenType.IDENTIFIER).value
        # TODO: Handle library imports
    
    def compile_init(self):
        """Compile: INIT environment <env>"""
        self.expect(TokenType.KEYWORD)  # 'INIT'
        self.expect(TokenType.KEYWORD)  # 'environment'
        env_name = self.expect(TokenType.IDENTIFIER).value
        # TODO: Initialize environment
    
    def compile_env_declaration(self):
        """Compile: env <name> <type> = <value>"""
        self.expect(TokenType.KEYWORD)  # 'env'
        var_name = self.expect(TokenType.IDENTIFIER).value
        
        # Variable initialization
        var_idx = self.bytecode.add_variable(var_name)
        
        # Type or direct assignment
        next_token = self.peek()
        if next_token.type == TokenType.DOUBLE_ASSIGN:  # env name << value
            self.advance()
            self.compile_expression()
            self.bytecode.emit(Opcode.STORE_VAR, var_idx)
        elif next_token.type == TokenType.IDENTIFIER:  # Type specified
            type_name = self.advance().value
            self.expect(TokenType.ASSIGN)
            self.compile_expression()
            self.bytecode.emit(Opcode.STORE_VAR, var_idx)
        else:
            self.error("Expected type or << in variable declaration")
    
    def compile_area(self):
        """Compile: area module main() open ... close"""
        self.expect(TokenType.KEYWORD)  # 'area'
        self.expect(TokenType.KEYWORD)  # 'module'
        func_name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.KEYWORD)  # 'open'
        
        func_start = len(self.bytecode.code)
        self.bytecode.functions[func_name] = func_start
        
        self.skip_newlines()
        self.compile_block()
        
        self.expect(TokenType.KEYWORD)  # 'close'
    
    def compile_module(self):
        """Compile: module <name>() open ... close"""
        self.expect(TokenType.KEYWORD)  # 'module'
        func_name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        # TODO: Parse parameters
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.KEYWORD)  # 'open'
        
        func_start = len(self.bytecode.code)
        self.bytecode.functions[func_name] = func_start
        
        self.skip_newlines()
        self.compile_block()
        
        self.expect(TokenType.KEYWORD)  # 'close'
        self.bytecode.emit(Opcode.RET)
    
    def compile_class(self):
        """Compile: class <name> open ... close"""
        self.expect(TokenType.KEYWORD)  # 'class'
        class_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.KEYWORD)  # 'open'
        
        self.skip_newlines()
        # TODO: Parse class members
        
        self.expect(TokenType.KEYWORD)  # 'close'
    
    def compile_block(self):
        """Compile a block of statements"""
        while self.peek() and self.peek().type != TokenType.EOF:
            self.skip_newlines()
            
            token = self.peek()
            if not token:
                break
            
            if token.type == TokenType.KEYWORD and token.value == 'close':
                break
            elif token.type == TokenType.KEYWORD:
                if token.value == 'if':
                    self.compile_if()
                elif token.value == 'for':
                    self.compile_for()
                elif token.value == 'while':
                    self.compile_while()
                elif token.value == 'switch':
                    self.compile_switch()
                elif token.value == 'try':
                    self.compile_try()
                elif token.value == 'back':
                    self.compile_return()
                elif token.value == 'stop':
                    self.advance()
                    # Convert to break
                elif token.value == 'continue':
                    self.advance()
                    # TODO: Emit continue
                elif token.value == 'env':
                    self.compile_env_declaration()
                elif token.value == 'pass':
                    self.advance()  # No-op
            else:
                # Try to parse as expression statement or function call
                self.compile_expression_statement()
            
            self.skip_newlines()
    
    def compile_expression_statement(self):
        """Compile an expression as a statement (like function calls)"""
        # Check if this is a function call
        token = self.peek()
        if token and token.type == TokenType.IDENTIFIER:
            name = self.advance().value
            
            # Check for function call
            if self.peek() and self.peek().type == TokenType.LPAREN:
                self.advance()  # consume (
                
                # Parse arguments
                args_count = 0
                while self.peek() and self.peek().type != TokenType.RPAREN:
                    self.compile_expression()
                    args_count += 1
                    
                    if self.peek() and self.peek().type == TokenType.COMMA:
                        self.advance()
                    elif self.peek() and self.peek().type != TokenType.RPAREN:
                        break
                
                self.expect(TokenType.RPAREN)
                
                # Emit special handling for built-in functions
                if name == 'output':
                    self.bytecode.emit(Opcode.OUTPUT)
                elif name == 'input':
                    self.bytecode.emit(Opcode.INPUT)
                else:
                    # User function call
                    func_idx = len(self.bytecode.functions) if name in self.bytecode.functions else 0
                    self.bytecode.emit(Opcode.CALL, func_idx)
            else:
                # Regular identifier - load as variable
                var_idx = self.bytecode.add_variable(name)
                self.bytecode.emit(Opcode.LOAD_VAR, var_idx)
        else:
            # Try as regular expression
            self.compile_expression()
    
    def compile_if(self):
        """Compile: if <condition> do ... end"""
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
    
    def compile_for(self):
        """Compile: for (var) on range(n) do ... end"""
        self.expect(TokenType.KEYWORD)  # 'for'
        self.expect(TokenType.LPAREN)
        var_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.KEYWORD)  # 'on'
        self.expect(TokenType.KEYWORD)  # 'range'
        self.expect(TokenType.LPAREN)
        self.compile_expression()
        self.expect(TokenType.RPAREN)
        
        self.expect(TokenType.KEYWORD)  # 'do'
        
        loop_start = len(self.bytecode.code)
        self.skip_newlines()
        self.compile_block()
        
        self.bytecode.emit(Opcode.JMP, loop_start)
        self.expect(TokenType.KEYWORD)  # 'end'
    
    def compile_while(self):
        """Compile: while (condition) do ... end"""
        self.expect(TokenType.KEYWORD)  # 'while'
        self.expect(TokenType.LPAREN)
        
        loop_start = len(self.bytecode.code)
        self.compile_condition()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.KEYWORD)  # 'do'
        
        jmp_if_false = len(self.bytecode.code)
        self.bytecode.emit(Opcode.JMP_IFNOT, 0)  # Placeholder
        
        self.skip_newlines()
        self.compile_block()
        
        self.bytecode.emit(Opcode.JMP, loop_start)
        self.bytecode.code[jmp_if_false + 1] = len(self.bytecode.code) & 0xFF
        
        self.expect(TokenType.KEYWORD)  # 'end'
    
    def compile_switch(self):
        """Compile: switch (expr) do ... end"""
        self.expect(TokenType.KEYWORD)  # 'switch'
        self.compile_expression()
        self.expect(TokenType.KEYWORD)  # 'do'
        # TODO: Implement switch compilation
        self.expect(TokenType.KEYWORD)  # 'end'
    
    def compile_try(self):
        """Compile: try do ... catch error do ... end"""
        self.expect(TokenType.KEYWORD)  # 'try'
        self.expect(TokenType.KEYWORD)  # 'do'
        self.skip_newlines()
        self.compile_block()
        self.expect(TokenType.KEYWORD)  # 'catch'
        # TODO: Handle error variable
        self.expect(TokenType.KEYWORD)  # 'do'
        self.skip_newlines()
        self.compile_block()
        self.expect(TokenType.KEYWORD)  # 'end'
    
    def compile_return(self):
        """Compile: back or back with <value>"""
        self.expect(TokenType.KEYWORD)  # 'back'
        next_token = self.peek()
        
        if next_token and next_token.type == TokenType.KEYWORD and next_token.value == 'with':
            self.advance()
            self.compile_expression()
        
        self.bytecode.emit(Opcode.RET)
    
    def compile_condition(self):
        """Compile a condition expression"""
        self.compile_expression()
    
    def compile_expression(self):
        """Compile an expression"""
        self.compile_or_expr()
    
    def compile_or_expr(self):
        self.compile_and_expr()
        while self.peek() and self.peek().value == 'or':
            self.advance()
            self.compile_and_expr()
            self.bytecode.emit(Opcode.OR_OP)
    
    def compile_and_expr(self):
        self.compile_equality()
        while self.peek() and self.peek().value == 'and':
            self.advance()
            self.compile_equality()
            self.bytecode.emit(Opcode.AND_OP)
    
    def compile_equality(self):
        self.compile_comparison()
        while self.peek() and self.peek().type in (TokenType.EQ, TokenType.NE):
            op_type = self.advance().type
            self.compile_comparison()
            if op_type == TokenType.EQ:
                self.bytecode.emit(Opcode.EQ)
            else:
                self.bytecode.emit(Opcode.NE)
    
    def compile_comparison(self):
        self.compile_additive()
        while self.peek() and self.peek().type in (TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op_type = self.advance().type
            self.compile_additive()
            if op_type == TokenType.LT:
                self.bytecode.emit(Opcode.LT)
            elif op_type == TokenType.LE:
                self.bytecode.emit(Opcode.LE)
            elif op_type == TokenType.GT:
                self.bytecode.emit(Opcode.GT)
            elif op_type == TokenType.GE:
                self.bytecode.emit(Opcode.GE)
    
    def compile_additive(self):
        self.compile_multiplicative()
        while self.peek() and self.peek().type in (TokenType.PLUS, TokenType.MINUS):
            op_type = self.advance().type
            self.compile_multiplicative()
            if op_type == TokenType.PLUS:
                self.bytecode.emit(Opcode.ADD)
            else:
                self.bytecode.emit(Opcode.SUB)
    
    def compile_multiplicative(self):
        self.compile_unary()
        while self.peek() and self.peek().type in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op_type = self.advance().type
            self.compile_unary()
            if op_type == TokenType.STAR:
                self.bytecode.emit(Opcode.MUL)
            elif op_type == TokenType.SLASH:
                self.bytecode.emit(Opcode.DIV)
            elif op_type == TokenType.PERCENT:
                self.bytecode.emit(Opcode.MOD)
    
    def compile_unary(self):
        token = self.peek()
        if token and token.type in (TokenType.MINUS, TokenType.NOT):
            op_type = self.advance().type
            self.compile_unary()
            if op_type == TokenType.MINUS:
                self.bytecode.emit(Opcode.NEG)
            elif op_type == TokenType.NOT:
                self.bytecode.emit(Opcode.NOT_OP)
        else:
            self.compile_primary()
    
    def compile_primary(self):
        token = self.peek()
        
        if not token:
            self.error("Unexpected end of input")
        
        if token.type == TokenType.INTEGER:
            self.advance()
            const_idx = self.bytecode.add_constant(int(token.value))
            self.bytecode.emit(Opcode.PUSH, const_idx)
        
        elif token.type == TokenType.FLOAT:
            self.advance()
            const_idx = self.bytecode.add_constant(float(token.value))
            self.bytecode.emit(Opcode.PUSH, const_idx)
        
        elif token.type == TokenType.STRING:
            self.advance()
            const_idx = self.bytecode.add_constant(token.value)
            self.bytecode.emit(Opcode.PUSH, const_idx)
        
        elif token.type == TokenType.BOOL:
            self.advance()
            const_idx = self.bytecode.add_constant(token.value == 'true')
            self.bytecode.emit(Opcode.PUSH, const_idx)
        
        elif token.type == TokenType.IDENTIFIER:
            name = self.advance().value
            var_idx = self.bytecode.add_variable(name)
            self.bytecode.emit(Opcode.LOAD_VAR, var_idx)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            self.compile_expression()
            self.expect(TokenType.RPAREN)
        
        else:
            self.error(f"Unexpected token in expression: {token.value}")

def compile_file(filename: str, output_filename: str):
    """Compile a Numium source file to bytecode"""
    with open(filename, 'r') as f:
        source = f.read()
    
    compiler = Compiler(source)
    bytecode = compiler.compile()
    bytecode.to_file(output_filename)
    
    print(f"Compiled {filename} -> {output_filename}")
    return bytecode
