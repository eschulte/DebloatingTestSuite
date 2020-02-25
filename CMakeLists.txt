# This is a master cmake script that will build all subprojects
# to produce a master list of binary test cases for ONR TPCP
# debloating research projects.
cmake_minimum_required (VERSION 3.10)
project (ONR_TPCP_TEST_SUITE)

# Submodules are built using ExternalProject
include(ExternalProject)

### ALL FINAL BUILT EXECUTABLES SHOULD BE PLACED IN THE FOLLOWING DIRECTORY:
# Either rename the executable to tell what build options were used,
# or place the executable in a subdirectory named based on build options
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/final-exe)

# Recurse into subdirectories.
# Two rules:
# (1) if subproject uses cmake, simply recurse into it
# (2) if does not use cmake, use a custom command to
#     call the subproject's Make script, etc.
#
# Examples below:
#
# ExternalProject_Add(yaml-cpp
#   EXCLUDE_FROM_ALL 1
#   SOURCE_DIR   ${REPO_DIR}/yaml-cpp
#   BINARY_DIR   ${BUILD_DIR}/yaml-cpp
#   INSTALL_DIR  ${FULL_STAGING_DIR}/yaml-cpp
#   CMAKE_ARGS
#   -DCMAKE_INSTALL_PREFIX=${FULL_STAGING_DIR}/yaml-cpp
#   -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=true -DYAML_CPP_BUILD_TESTS=false
#   -DYAML_CPP_BUILD_TOOLS=false -DYAML_CPP_BUILD_CONTRIB=false)
# ---- or ----
# ExternalProject_Add(boost
#   EXCLUDE_FROM_ALL 1
#   SOURCE_DIR   ${REPO_DIR}/boost
#   INSTALL_DIR  ${FULL_STAGING_DIR}/boost
#   EXCLUDE_FROM_ALL 1
#   CONFIGURE_COMMAND ./bootstrap.sh "--prefix=${FULL_STAGING_DIR}/boost"
#   --with-libraries=${BOOST_LIBRARIES_COMMA_SEP}
#   BUILD_IN_SOURCE true
#   BUILD_COMMAND ./b2 ${BOOST_B2_ARGS} headers
#   INSTALL_COMMAND ./b2 ${BOOST_B2_ARGS} install)

ExternalProject_Add(sqlite
  SOURCE_DIR   ${CMAKE_SOURCE_DIR}/sqlite
  BINARY_DIR   ${CMAKE_BINARY_DIR}/sqlite-build
  CONFIGURE_COMMAND ${CMAKE_SOURCE_DIR}/sqlite/configure
  BUILD_COMMAND make && make sqlite3.c
  INSTALL_COMMAND cp ${CMAKE_BINARY_DIR}/sqlite-build/sqlite3 ${CMAKE_BINARY_DIR}/final-exe/sqlite3_$ENV{TPCP_OPTIONS})
  
ExternalProject_Add(tar
  SOURCE_DIR   ${CMAKE_SOURCE_DIR}/tar-1.32
  BINARY_DIR   ${CMAKE_BINARY_DIR}/tar-build
  CONFIGURE_COMMAND ${CMAKE_SOURCE_DIR}/tar-1.32/configure
  BUILD_COMMAND make
  INSTALL_COMMAND cp ${CMAKE_BINARY_DIR}/tar-build/src/tar ${CMAKE_BINARY_DIR}/final-exe/tar_$ENV{TPCP_OPTIONS})


# file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/sqlite-build)
# add_custom_command(OUTPUT ${CMAKE_BINARY_DIR}/sqlite-build/sqlite3
#                    COMMAND ${CMAKE_SOURCE_DIR}/sqlite/configure
#                    COMMAND make
#                    COMMAND make sqlite3.c
#                    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/sqlite-build
#                    COMMENT "Building sqlite"
#                    )
# add_custom_target(sqlite
#                   DEPENDS ${CMAKE_BINARY_DIR}/sqlite-build/sqlite3
#                   )
#add_executable(sqlite)
# target_link_libraries(myexecutable full_path_to_generated_library)
#add_dependencies(sqlite sqlite-cmd)
