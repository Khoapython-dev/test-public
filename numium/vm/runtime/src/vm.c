/*
 * Numium Virtual Machine Implementation
 */

#include "../include/vm.h"
#include <string.h>
#include <math.h>

/* Value utility functions */
Value value_int(int64_t i) {
    Value v;
    v.type = VAL_INTEGER;
    v.data.i = i;
    return v;
}

Value value_float(double f) {
    Value v;
    v.type = VAL_FLOAT;
    v.data.f = f;
    return v;
}

Value value_string(const char* s) {
    Value v;
    v.type = VAL_STRING;
    v.data.s = malloc(strlen(s) + 1);
    strcpy(v.data.s, s);
    return v;
}

Value value_bool(bool b) {
    Value v;
    v.type = VAL_BOOL;
    v.data.i = b ? 1 : 0;
    return v;
}

Value value_null() {
    Value v;
    v.type = VAL_NULL;
    return v;
}

char* value_to_string(Value v) {
    char* result = malloc(256);
    switch (v.type) {
        case VAL_INTEGER:
            snprintf(result, 256, "%ld", v.data.i);
            break;
        case VAL_FLOAT:
            snprintf(result, 256, "%f", v.data.f);
            break;
        case VAL_STRING:
            strcpy(result, v.data.s);
            break;
        case VAL_BOOL:
            strcpy(result, v.data.i ? "true" : "false");
            break;
        case VAL_NULL:
            strcpy(result, "null");
            break;
        default:
            strcpy(result, "<unknown>");
    }
    return result;
}

void value_free(Value v) {
    if (v.type == VAL_STRING && v.data.s) {
        free(v.data.s);
    }
}

/* VM Creation and Destruction */
VM* vm_create() {
    VM* vm = malloc(sizeof(VM));
    vm->code = NULL;
    vm->code_size = 0;
    vm->pc = 0;
    
    vm->stack = malloc(sizeof(Value) * STACK_SIZE);
    vm->stack_ptr = 0;
    
    vm->variables = malloc(sizeof(Value) * MAX_VARIABLES);
    vm->var_count = 0;
    
    vm->constants.values = malloc(sizeof(Value) * 256);
    vm->constants.count = 0;
    vm->constants.capacity = 256;
    
    vm->memory = malloc(MEMORY_SIZE);
    vm->memory_ptr = 0;
    
    vm->func_count = 0;
    vm->halted = false;
    vm->exit_code = 0;
    
    return vm;
}

void vm_destroy(VM* vm) {
    if (vm) {
        if (vm->code) free(vm->code);
        if (vm->stack) free(vm->stack);
        if (vm->variables) free(vm->variables);
        if (vm->memory) free(vm->memory);
        
        // Free constants
        for (size_t i = 0; i < vm->constants.count; i++) {
            value_free(vm->constants.values[i]);
        }
        if (vm->constants.values) free(vm->constants.values);
        
        free(vm);
    }
}

/* Load bytecode from file */
int vm_load_bytecode(VM* vm, const char* filename) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        fprintf(stderr, "Error: Cannot open bytecode file %s\n", filename);
        return -1;
    }
    
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    vm->code = malloc(size);
    vm->code_size = size;
    
    if (fread(vm->code, 1, size, file) != (size_t)size) {
        fprintf(stderr, "Error: Failed to read bytecode file\n");
        fclose(file);
        return -1;
    }
    
    fclose(file);
    printf("Loaded bytecode: %ld bytes\n", size);
    return 0;
}

/* Stack operations */
void vm_push(VM* vm, Value value) {
    if (vm->stack_ptr >= STACK_SIZE) {
        fprintf(stderr, "Error: Stack overflow\n");
        vm->halted = true;
        return;
    }
    vm->stack[vm->stack_ptr++] = value;
}

Value vm_pop(VM* vm) {
    if (vm->stack_ptr == 0) {
        fprintf(stderr, "Error: Stack underflow\n");
        vm->halted = true;
        return value_null();
    }
    return vm->stack[--vm->stack_ptr];
}

Value vm_peek(VM* vm) {
    if (vm->stack_ptr == 0) {
        fprintf(stderr, "Error: Stack empty\n");
        return value_null();
    }
    return vm->stack[vm->stack_ptr - 1];
}

/* Arithmetic operations */
Value vm_add(Value a, Value b) {
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_int(a.data.i + b.data.i);
    } else if (a.type == VAL_FLOAT || b.type == VAL_FLOAT) {
        double fa = (a.type == VAL_FLOAT) ? a.data.f : a.data.i;
        double fb = (b.type == VAL_FLOAT) ? b.data.f : b.data.i;
        return value_float(fa + fb);
    } else if (a.type == VAL_STRING && b.type == VAL_STRING) {
        char* result = malloc(strlen(a.data.s) + strlen(b.data.s) + 1);
        sprintf(result, "%s%s", a.data.s, b.data.s);
        Value v = value_string(result);
        free(result);
        return v;
    }
    return value_null();
}

Value vm_sub(Value a, Value b) {
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_int(a.data.i - b.data.i);
    } else if (a.type == VAL_FLOAT || b.type == VAL_FLOAT) {
        double fa = (a.type == VAL_FLOAT) ? a.data.f : a.data.i;
        double fb = (b.type == VAL_FLOAT) ? b.data.f : b.data.i;
        return value_float(fa - fb);
    }
    return value_null();
}

Value vm_mul(Value a, Value b) {
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_int(a.data.i * b.data.i);
    } else if (a.type == VAL_FLOAT || b.type == VAL_FLOAT) {
        double fa = (a.type == VAL_FLOAT) ? a.data.f : a.data.i;
        double fb = (b.type == VAL_FLOAT) ? b.data.f : b.data.i;
        return value_float(fa * fb);
    }
    return value_null();
}

Value vm_div(Value a, Value b) {
    if (b.type == VAL_INTEGER && b.data.i == 0) {
        fprintf(stderr, "Error: Division by zero\n");
        return value_null();
    }
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_int(a.data.i / b.data.i);
    } else if (a.type == VAL_FLOAT || b.type == VAL_FLOAT) {
        double fa = (a.type == VAL_FLOAT) ? a.data.f : a.data.i;
        double fb = (b.type == VAL_FLOAT) ? b.data.f : b.data.i;
        return value_float(fa / fb);
    }
    return value_null();
}

Value vm_mod(Value a, Value b) {
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_int(a.data.i % b.data.i);
    }
    return value_null();
}

Value vm_neg(Value a) {
    if (a.type == VAL_INTEGER) {
        return value_int(-a.data.i);
    } else if (a.type == VAL_FLOAT) {
        return value_float(-a.data.f);
    }
    return value_null();
}

/* Comparison operations */
Value vm_eq(Value a, Value b) {
    if (a.type != b.type) return value_bool(false);
    
    switch (a.type) {
        case VAL_INTEGER:
            return value_bool(a.data.i == b.data.i);
        case VAL_FLOAT:
            return value_bool(fabs(a.data.f - b.data.f) < 1e-9);
        case VAL_STRING:
            return value_bool(strcmp(a.data.s, b.data.s) == 0);
        case VAL_BOOL:
            return value_bool(a.data.i == b.data.i);
        default:
            return value_bool(false);
    }
}

Value vm_ne(Value a, Value b) {
    Value eq_result = vm_eq(a, b);
    return value_bool(!eq_result.data.i);
}

Value vm_lt(Value a, Value b) {
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_bool(a.data.i < b.data.i);
    } else if (a.type == VAL_FLOAT || b.type == VAL_FLOAT) {
        double fa = (a.type == VAL_FLOAT) ? a.data.f : a.data.i;
        double fb = (b.type == VAL_FLOAT) ? b.data.f : b.data.i;
        return value_bool(fa < fb);
    }
    return value_bool(false);
}

Value vm_le(Value a, Value b) {
    Value lt = vm_lt(a, b);
    Value eq = vm_eq(a, b);
    return value_bool(lt.data.i || eq.data.i);
}

Value vm_gt(Value a, Value b) {
    if (a.type == VAL_INTEGER && b.type == VAL_INTEGER) {
        return value_bool(a.data.i > b.data.i);
    } else if (a.type == VAL_FLOAT || b.type == VAL_FLOAT) {
        double fa = (a.type == VAL_FLOAT) ? a.data.f : a.data.i;
        double fb = (b.type == VAL_FLOAT) ? b.data.f : b.data.i;
        return value_bool(fa > fb);
    }
    return value_bool(false);
}

Value vm_ge(Value a, Value b) {
    Value gt = vm_gt(a, b);
    Value eq = vm_eq(a, b);
    return value_bool(gt.data.i || eq.data.i);
}

/* Logic operations */
Value vm_and(Value a, Value b) {
    bool a_bool = (a.type == VAL_BOOL || (a.type == VAL_INTEGER && a.data.i != 0));
    bool b_bool = (b.type == VAL_BOOL || (b.type == VAL_INTEGER && b.data.i != 0));
    return value_bool(a_bool && b_bool);
}

Value vm_or(Value a, Value b) {
    bool a_bool = (a.type == VAL_BOOL || (a.type == VAL_INTEGER && a.data.i != 0));
    bool b_bool = (b.type == VAL_BOOL || (b.type == VAL_INTEGER && b.data.i != 0));
    return value_bool(a_bool || b_bool);
}

Value vm_not(Value a) {
    bool a_bool = (a.type == VAL_BOOL || (a.type == VAL_INTEGER && a.data.i != 0));
    return value_bool(!a_bool);
}

/* I/O operations */
void vm_output(Value value) {
    char* str = value_to_string(value);
    printf("%s", str);
    free(str);
}

Value vm_input() {
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        return value_string(buffer);
    }
    return value_null();
}

/* Main VM execution loop */
int vm_run(VM* vm) {
    if (!vm->code) {
        fprintf(stderr, "Error: No bytecode loaded\n");
        return -1;
    }
    
    printf("Starting VM execution...\n");
    
    while (!vm->halted && vm->pc < vm->code_size) {
        uint8_t opcode = vm->code[vm->pc++];
        
        switch (opcode) {
            case OP_HALT:
                vm->halted = true;
                break;
            
            case OP_NOP:
                break;
            
            case OP_PUSH: {
                uint32_t arg = 0;
                if (vm->pc + 3 < vm->code_size) {
                    arg = vm->code[vm->pc] | 
                          (vm->code[vm->pc + 1] << 8) |
                          (vm->code[vm->pc + 2] << 16) |
                          (vm->code[vm->pc + 3] << 24);
                    vm->pc += 4;
                }
                // Push constant from constant pool
                if (arg < vm->constants.count) {
                    vm_push(vm, vm->constants.values[arg]);
                } else {
                    // Fallback: push as integer
                    vm_push(vm, value_int(arg));
                }
                break;
            }
            
            case OP_POP:
                vm_pop(vm);
                break;
            
            case OP_DUP: {
                Value v = vm_peek(vm);
                vm_push(vm, v);
                break;
            }
            
            case OP_ADD: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_add(a, b));
                break;
            }
            
            case OP_SUB: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_sub(a, b));
                break;
            }
            
            case OP_MUL: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_mul(a, b));
                break;
            }
            
            case OP_DIV: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_div(a, b));
                break;
            }
            
            case OP_MOD: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_mod(a, b));
                break;
            }
            
            case OP_NEG: {
                Value a = vm_pop(vm);
                vm_push(vm, vm_neg(a));
                break;
            }
            
            case OP_EQ: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_eq(a, b));
                break;
            }
            
            case OP_NE: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_ne(a, b));
                break;
            }
            
            case OP_LT: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_lt(a, b));
                break;
            }
            
            case OP_LE: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_le(a, b));
                break;
            }
            
            case OP_GT: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_gt(a, b));
                break;
            }
            
            case OP_GE: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_ge(a, b));
                break;
            }
            
            case OP_AND: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_and(a, b));
                break;
            }
            
            case OP_OR: {
                Value b = vm_pop(vm);
                Value a = vm_pop(vm);
                vm_push(vm, vm_or(a, b));
                break;
            }
            
            case OP_NOT: {
                Value a = vm_pop(vm);
                vm_push(vm, vm_not(a));
                break;
            }
            
            case OP_OUTPUT: {
                Value v = vm_pop(vm);
                vm_output(v);
                break;
            }
            
            default:
                fprintf(stderr, "Error: Unknown opcode 0x%02X at position %u\n", opcode, vm->pc - 1);
                vm->halted = true;
                return -1;
        }
    }
    
    printf("\nVM execution completed\n");
    return vm->exit_code;
}

void vm_dump_state(VM* vm) {
    printf("=== VM State ===\n");
    printf("PC: %u / Code size: %zu\n", vm->pc, vm->code_size);
    printf("Stack pointer: %zu / Stack size: %d\n", vm->stack_ptr, STACK_SIZE);
    printf("Variables: %zu\n", vm->var_count);
    printf("Constants: %zu\n", vm->constants.count);
    printf("Halted: %s\n", vm->halted ? "true" : "false");
}

/* Add constant to pool */
int vm_add_constant(VM* vm, Value value) {
    if (vm->constants.count >= vm->constants.capacity) {
        vm->constants.capacity *= 2;
        vm->constants.values = realloc(vm->constants.values, sizeof(Value) * vm->constants.capacity);
    }
    int idx = vm->constants.count++;
    vm->constants.values[idx] = value;
    return idx;
}

/* Load metadata from JSON (simple parser) */
int vm_load_metadata(VM* vm, const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        return 0;  // No metadata file - not an error
    }
    
    // Simple metadata loading - just read constants array
    char line[1024];
    while (fgets(line, sizeof(line), file)) {
        // Look for string constants
        if (strchr(line, '"')) {
            // Extract string between quotes
            char* start = strchr(line, '"');
            if (start) {
                start++;
                char* end = strchr(start, '"');
                if (end && start != end) {
                    char constant[512];
                    int len = end - start;
                    strncpy(constant, start, len);
                    constant[len] = '\0';
                    
                    // Handle escape sequences
                    char* decoded = malloc(len + 100);
                    int j = 0;
                    for (int i = 0; i < len; i++) {
                        if (constant[i] == '\\' && i + 1 < len) {
                            if (constant[i+1] == 'n') {
                                decoded[j++] = '\n';
                                i++;
                            } else if (constant[i+1] == 't') {
                                decoded[j++] = '\t';
                                i++;
                            } else if (constant[i+1] == '\\') {
                                decoded[j++] = '\\';
                                i++;
                            } else {
                                decoded[j++] = constant[i];
                            }
                        } else {
                            decoded[j++] = constant[i];
                        }
                    }
                    decoded[j] = '\0';
                    
                    // Add to constant pool (skip metadata keys)
                    if (strcmp(constant, "version") != 0 && 
                        strcmp(constant, "constants") != 0 &&
                        strcmp(constant, "variables") != 0 &&
                        strcmp(constant, "functions") != 0) {
                        vm_add_constant(vm, value_string(decoded));
                    }
                    free(decoded);
                }
            }
        }
    }
    fclose(file);
    return 0;
}
