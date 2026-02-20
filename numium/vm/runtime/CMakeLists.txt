cmake_minimum_required(VERSION 3.10)
project(numium_vm C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Source files
set(VM_SOURCES
    src/vm.c
    src/main.c
)

set(VM_HEADERS
    include/vm.h
)

# Create executable
add_executable(numium_vm ${VM_SOURCES} ${VM_HEADERS})

# Include directories
target_include_directories(numium_vm PRIVATE include)

# Compiler flags
if(MSVC)
    target_compile_options(numium_vm PRIVATE /W4)
else()
    target_compile_options(numium_vm PRIVATE -Wall -Wextra -Wpedantic)
endif()

# Install
install(TARGETS numium_vm DESTINATION bin)
