cmake_minimum_required(VERSION 3.15)
project(ORToolsExample CXX)

# --- C++ standard ---
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# --- Ensure OR_PROTO_DLL is empty to fix protobuf macros on macOS ---
add_definitions(-DOR_PROTO_DLL=)

# --- Find Abseil (Homebrew) ---
find_package(absl REQUIRED)
if(NOT absl_FOUND)
    message(FATAL_ERROR "Abseil not found. Install via Homebrew: brew install abseil")
endif()

find_package(Protobuf REQUIRED)
if(NOT Protobuf_FOUND)
    message(FATAL_ERROR "Protobuf not found. Install via Homebrew: brew install protobuf")
endif()

# --- OR-Tools --- (either hard code the path to or-tools in brew)
# set(ORTOOLS_ROOT "/opt/homebrew/opt/or-tools")

# Detect Homebrew prefix automatically (or detect automatically)
execute_process(
    COMMAND brew --prefix or-tools
    OUTPUT_VARIABLE ORTOOLS_ROOT
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

include_directories(${ORTOOLS_ROOT}/include)
link_directories(${ORTOOLS_ROOT}/lib)

# --- Create executable ---
add_executable(ortools_example src/ortools.cpp)

target_include_directories(ortools_example PRIVATE ${Protobuf_INCLUDE_DIRS})
target_link_libraries(ortools_example PRIVATE ${Protobuf_LIBRARIES})

# --- Link libraries ---
target_link_libraries(ortools_example PRIVATE
    absl::base
    absl::log
    absl::log_globals
    absl::log_severity
    absl::log_initialize
    absl::flags
    absl::flags_parse
    absl::flags_usage
    absl::strings
    absl::check
    absl::log_internal_check_impl
    absl::log_internal_check_op
    absl::log_internal_message
    absl::synchronization
    absl::time
    absl::status
    absl::statusor
    ${ORTOOLS_ROOT}/lib/libortools.dylib
)

# --- Set runtime library path so dylib can be found at runtime ---
set_target_properties(ortools_example PROPERTIES
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "${ORTOOLS_ROOT}/lib"
)
