# ===== CMAKE SETTINGS =====
# Minimum version
cmake_minimum_required(VERSION 2.8)

# Compilation flags
set(CMAKE_CXX_COMPILER "clang")
set(CMAKE_CXX_FLAGS "-g -Wall")

# Linking flags
LINK_DIRECTORIES(${CMAKE_SOURCE_DIR}/../../lib/})

# Set output paths
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/../bin/)
set(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/../lib/)

# Define and include some useful paths
set(PROJECT_SOURCE_DIR ${CMAKE_SOURCE_DIR})
set(EXEC_DIR ${PROJECT_SOURCE_DIR}/Executables)
set(GENERIC_DIR ${PROJECT_SOURCE_DIR}/Generic)
set(MODULES_DIR ${PROJECT_SOURCE_DIR}/Modules)

include_directories(${PROJECT_SOURCE_DIR})
include_directories(${GENERIC_DIR})

# ===== ADD LIBRARIES =====
# Generic libraries

# Module libraries
add_subdirectory(${MODULES_DIR}/Audio)
add_subdirectory(${MODULES_DIR}/Skeleton)

# ===== ADD EXECUTABLES =====
# Console synth (no GUI)
add_subdirectory(${EXEC_DIR}/CLISynth)

# Main application

