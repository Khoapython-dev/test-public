"""
Numium Lexer - Tokenize source code
Phân tích từ vựng cho ngôn ngữ Numium
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    HEX64 = auto()
    CHAR = auto()
    
    # Keywords
    KEYWORD = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Operators
    ASSIGN = auto()           # =
    DOUBLE_ASSIGN = auto()     # <<
    PLUS = auto()              # +
    MINUS = auto()             # -
    STAR = auto()              # *
    SLASH = auto()             # /
    PERCENT = auto()           # %
    EQ = auto()                # ==
    NE = auto()                # !=
    LT = auto()                # <
    LE = auto()                # <=
    GT = auto()                # >
    GE = auto()                # >=
    AND = auto()               # &&
    OR = auto()                # ||
    NOT = auto()               # !
    
    # Delimiters
    LPAREN = auto()            # (
    RPAREN = auto()            # )
    LBRACKET = auto()          # [
    RBRACKET = auto()          # ]
    COMMA = auto()             # ,
    COLON = auto()             # :
    DOT = auto()               # .
    DOLLAR = auto()            # $
    DOUBLE_COLON = auto()      # ::
    
    # Special
    NEWLINE = auto()
    EOF = auto()
    COMMENT = auto()

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    KEYWORDS = {
        'open', 'close', 'do', 'end',
        'if', 'else', 'for', 'while', 'switch', 'case', 'try', 'catch',
        'area', 'module', 'class', 'region', 'database', 'event',
        'private', 'public',
        'import', 'INIT', 'START', 'environment',
        'env', 'back', 'with', 'pass', 'stop', 'continue',
        'and', 'or', 'not',
        'on', 'in', 'range',
        'local', 'call',
        'true', 'false',
        'int', 'float', 'string', 'under_int', 'hex64', 'char', 'bool', 'list', 'dict', 'activate',
    }
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def error(self, message: str):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.position + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.position < len(self.source):
            char = self.source[self.position]
            self.position += 1
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return char
        return None
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num_str = ''
        
        # Check for hex
        if self.peek() == '0' and self.peek(1) == 'x':
            self.advance()
            self.advance()
            while self.peek() and self.peek() in '0123456789abcdefABCDEF':
                num_str += self.peek()
                self.advance()
            return Token(TokenType.HEX64, '0x' + num_str, start_line, start_col)
        
        # Regular number
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.peek()
            self.advance()
        
        if '.' in num_str:
            return Token(TokenType.FLOAT, num_str, start_line, start_col)
        return Token(TokenType.INTEGER, num_str, start_line, start_col)
    
    def read_string(self, quote: str) -> Token:
        start_line, start_col = self.line, self.column
        self.advance()  # Skip opening quote
        string_val = ''
        
        while self.peek() and self.peek() != quote:
            if self.peek() == '\\':
                self.advance()
                escaped = self.peek()
                if escaped == 'n':
                    string_val += '\n'
                elif escaped == 't':
                    string_val += '\t'
                elif escaped == '\\':
                    string_val += '\\'
                elif escaped == quote:
                    string_val += quote
                else:
                    string_val += escaped
                self.advance()
            else:
                string_val += self.peek()
                self.advance()
        
        if not self.peek():
            self.error(f"Unterminated string starting at line {start_line}")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_val, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        ident = ''
        
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.peek()
            self.advance()
        
        if ident in self.KEYWORDS:
            return Token(TokenType.KEYWORD, ident, start_line, start_col)
        if ident in ('true', 'false'):
            return Token(TokenType.BOOL, ident, start_line, start_col)
        
        return Token(TokenType.IDENTIFIER, ident, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            current = self.peek()
            start_line, start_col = self.line, self.column
            
            # Comments
            if current == '#':
                while self.peek() and self.peek() != '\n':
                    self.advance()
                continue
            
            # Newline
            if current == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', start_line, start_col))
                self.advance()
                continue
            
            # Strings
            if current in ('"', "'"):
                self.tokens.append(self.read_string(current))
                continue
            
            # Numbers
            if current.isdigit():
                self.tokens.append(self.read_number())
                continue
            
            # Identifiers and keywords
            if current.isalpha() or current == '_':
                self.tokens.append(self.read_identifier())
                continue
            
            # Operators and delimiters
            if current == '=' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.EQ, '==', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '!' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.NE, '!=', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '<' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.LE, '<=', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '<' and self.peek(1) == '<':
                self.tokens.append(Token(TokenType.DOUBLE_ASSIGN, '<<', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '>' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.GE, '>=', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '&' and self.peek(1) == '&':
                self.tokens.append(Token(TokenType.AND, '&&', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '|' and self.peek(1) == '|':
                self.tokens.append(Token(TokenType.OR, '||', start_line, start_col))
                self.advance()
                self.advance()
            elif current == ':' and self.peek(1) == ':':
                self.tokens.append(Token(TokenType.DOUBLE_COLON, '::', start_line, start_col))
                self.advance()
                self.advance()
            elif current == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col))
                self.advance()
            elif current == '<':
                self.tokens.append(Token(TokenType.LT, '<', start_line, start_col))
                self.advance()
            elif current == '>':
                self.tokens.append(Token(TokenType.GT, '>', start_line, start_col))
                self.advance()
            elif current == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
                self.advance()
            elif current == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
                self.advance()
            elif current == '*':
                self.tokens.append(Token(TokenType.STAR, '*', start_line, start_col))
                self.advance()
            elif current == '/':
                self.tokens.append(Token(TokenType.SLASH, '/', start_line, start_col))
                self.advance()
            elif current == '%':
                self.tokens.append(Token(TokenType.PERCENT, '%', start_line, start_col))
                self.advance()
            elif current == '!':
                self.tokens.append(Token(TokenType.NOT, '!', start_line, start_col))
                self.advance()
            elif current == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
                self.advance()
            elif current == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
                self.advance()
            elif current == '[':
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col))
                self.advance()
            elif current == ']':
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col))
                self.advance()
            elif current == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
                self.advance()
            elif current == ':':
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_col))
                self.advance()
            elif current == '.':
                self.tokens.append(Token(TokenType.DOT, '.', start_line, start_col))
                self.advance()
            elif current == '$':
                self.tokens.append(Token(TokenType.DOLLAR, '$', start_line, start_col))
                self.advance()
            else:
                self.error(f"Unexpected character: {current}")
        
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
