/*
 * Numium VM Main Entry Point
 */

#include "../include/vm.h"
#include <string.h>
#include <stdio.h>

void print_usage(const char* program) {
    printf("Usage: %s <bytecode_file>\n", program);
    printf("       %s --help\n", program);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }
    
    if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0) {
        print_usage(argv[0]);
        printf("\nNumium Virtual Machine v0.1\n");
        printf("Execute Numium bytecode files compiled from .num source files\n");
        return 0;
    }
    
    const char* bytecode_file = argv[1];
    
    printf("Numium Virtual Machine v0.1\n");
    printf("Loading bytecode: %s\n\n", bytecode_file);
    
    VM* vm = vm_create();
    
    if (vm_load_bytecode(vm, bytecode_file) != 0) {
        vm_destroy(vm);
        return 1;
    }
    
    // Load metadata (constants) if available
    char metadata_file[512];
    snprintf(metadata_file, sizeof(metadata_file), "%s", bytecode_file);
    char* dot = strrchr(metadata_file, '.');
    if (dot) {
        *dot = '\0';
        strcat(metadata_file, ".meta.json");
        vm_load_metadata(vm, metadata_file);
    }
    
    int result = vm_run(vm);
    
    if (argc >= 3 && strcmp(argv[2], "--debug") == 0) {
        vm_dump_state(vm);
    }
    
    vm_destroy(vm);
    
    return result;
}

