/*
 * Numium Virtual Machine
 * Header file for VM execution engine
 */

#ifndef NUMIUM_VM_H
#define NUMIUM_VM_H

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define STACK_SIZE 1024
#define MEMORY_SIZE 65536
#define MAX_VARIABLES 256
#define MAX_FUNCTIONS 64

/* Opcode definitions */
#define OP_PUSH 0x01
#define OP_POP 0x02
#define OP_DUP 0x03
#define OP_ADD 0x10
#define OP_SUB 0x11
#define OP_MUL 0x12
#define OP_DIV 0x13
#define OP_MOD 0x14
#define OP_NEG 0x15
#define OP_EQ 0x20
#define OP_NE 0x21
#define OP_LT 0x22
#define OP_LE 0x23
#define OP_GT 0x24
#define OP_GE 0x25
#define OP_AND 0x30
#define OP_OR 0x31
#define OP_NOT 0x32
#define OP_LOAD_VAR 0x40
#define OP_STORE_VAR 0x41
#define OP_INIT_VAR 0x42
#define OP_JMP 0x50
#define OP_JMP_IF 0x51
#define OP_JMP_IFNOT 0x52
#define OP_CALL 0x53
#define OP_RET 0x54
#define OP_OUTPUT 0x60
#define OP_INPUT 0x61
#define OP_MAKE_LIST 0x70
#define OP_MAKE_DICT 0x71
#define OP_LIST_GET 0x72
#define OP_LIST_SET 0x73
#define OP_DICT_GET 0x74
#define OP_DICT_SET 0x75
#define OP_NOP 0xFF
#define OP_HALT 0x00

/* Value types */
typedef enum {
    VAL_INTEGER,
    VAL_FLOAT,
    VAL_STRING,
    VAL_BOOL,
    VAL_LIST,
    VAL_DICT,
    VAL_NULL
} ValueType;

/* Value structure */
typedef struct {
    ValueType type;
    union {
        int64_t i;
        double f;
        char* s;
        struct {
            void** items;
            size_t count;
        } list;
        struct {
            char** keys;
            void** values;
            size_t count;
        } dict;
    } data;
} Value;
/* Constant pool */
typedef struct {
    Value* values;
    size_t count;
    size_t capacity;
} ConstantPool;
/* Function entry */
typedef struct {
    uint8_t* code;
    size_t code_size;
    uint32_t entry_point;
} Function;

/* Virtual Machine state */
typedef struct {
    uint8_t* code;
    size_t code_size;
    uint32_t pc;              /* Program counter */
    
    Value* stack;
    size_t stack_ptr;
    
    Value* variables;
    size_t var_count;
    
    ConstantPool constants;
    
    Function functions[MAX_FUNCTIONS];
    size_t func_count;
    
    uint8_t* memory;
    size_t memory_ptr;
    
    bool halted;
    int exit_code;
} VM;

/* Function declarations */
VM* vm_create();
void vm_destroy(VM* vm);
int vm_load_bytecode(VM* vm, const char* filename);
int vm_add_constant(VM* vm, Value value);
int vm_load_metadata(VM* vm, const char* filename);
int vm_run(VM* vm);
void vm_dump_state(VM* vm);

/* Stack operations */
void vm_push(VM* vm, Value value);
Value vm_pop(VM* vm);
Value vm_peek(VM* vm);

/* Arithmetic operations */
Value vm_add(Value a, Value b);
Value vm_sub(Value a, Value b);
Value vm_mul(Value a, Value b);
Value vm_div(Value a, Value b);
Value vm_mod(Value a, Value b);
Value vm_neg(Value a);

/* Comparison operations */
Value vm_eq(Value a, Value b);
Value vm_ne(Value a, Value b);
Value vm_lt(Value a, Value b);
Value vm_le(Value a, Value b);
Value vm_gt(Value a, Value b);
Value vm_ge(Value a, Value b);

/* Logic operations */
Value vm_and(Value a, Value b);
Value vm_or(Value a, Value b);
Value vm_not(Value a);

/* I/O operations */
void vm_output(Value value);
Value vm_input();

/* Value utility functions */
Value value_int(int64_t i);
Value value_float(double f);
Value value_string(const char* s);
Value value_bool(bool b);
Value value_null();
char* value_to_string(Value v);
void value_free(Value v);

#endif
