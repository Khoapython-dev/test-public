"""
Numium Bytecode Opcodes Definition
Định nghĩa các opcode cho VM Numium
"""

class Opcode:
    """Danh sách tất cả opcodes"""
    
    # Stack operations
    PUSH = 0x01          # Push value onto stack
    POP = 0x02           # Pop value from stack
    DUP = 0x03           # Duplicate top stack value
    
    # Arithmetic
    ADD = 0x10           # Addition
    SUB = 0x11           # Subtraction
    MUL = 0x12           # Multiplication
    DIV = 0x13           # Division
    MOD = 0x14           # Modulo
    NEG = 0x15           # Negate
    
    # Comparison
    EQ = 0x20            # Equal
    NE = 0x21            # Not equal
    LT = 0x22            # Less than
    LE = 0x23            # Less than or equal
    GT = 0x24            # Greater than
    GE = 0x25            # Greater than or equal
    
    # Logic
    AND_OP = 0x30        # Logical AND
    OR_OP = 0x31         # Logical OR
    NOT_OP = 0x32        # Logical NOT
    
    # Variables
    LOAD_VAR = 0x40      # Load variable
    STORE_VAR = 0x41     # Store to variable
    INIT_VAR = 0x42      # Initialize variable
    
    # Control Flow
    JMP = 0x50           # Jump
    JMP_IF = 0x51        # Jump if true
    JMP_IFNOT = 0x52     # Jump if false
    CALL = 0x53          # Call function
    RET = 0x54           # Return from function
    
    # I/O
    OUTPUT = 0x60        # Print to output
    INPUT = 0x61         # Read from input
    
    # Data structures
    MAKE_LIST = 0x70     # Create list
    MAKE_DICT = 0x71     # Create dictionary
    LIST_GET = 0x72      # Get list element
    LIST_SET = 0x73      # Set list element
    DICT_GET = 0x74      # Get dict value
    DICT_SET = 0x75      # Set dict value
    
    # Special
    NOP = 0xFF           # No operation
    HALT = 0x00          # Stop execution

# Opcode names for debugging
OPCODE_NAMES = {
    0x01: "PUSH",
    0x02: "POP",
    0x03: "DUP",
    0x10: "ADD",
    0x11: "SUB",
    0x12: "MUL",
    0x13: "DIV",
    0x14: "MOD",
    0x15: "NEG",
    0x20: "EQ",
    0x21: "NE",
    0x22: "LT",
    0x23: "LE",
    0x24: "GT",
    0x25: "GE",
    0x30: "AND",
    0x31: "OR",
    0x32: "NOT",
    0x40: "LOAD_VAR",
    0x41: "STORE_VAR",
    0x42: "INIT_VAR",
    0x50: "JMP",
    0x51: "JMP_IF",
    0x52: "JMP_IFNOT",
    0x53: "CALL",
    0x54: "RET",
    0x60: "OUTPUT",
    0x61: "INPUT",
    0x70: "MAKE_LIST",
    0x71: "MAKE_DICT",
    0x72: "LIST_GET",
    0x73: "LIST_SET",
    0x74: "DICT_GET",
    0x75: "DICT_SET",
    0xFF: "NOP",
    0x00: "HALT",
}
