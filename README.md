# TPCP Debloating Test Suite #

This repository contains test programs for TPCP. The test programs are
meant to support the development of debloating tools that analyze
native binaries. The example test cases are selected using a number of different
dimensions, such as size, number of components, and configurability.

## Test Program Options ##

Each test program is compiled for numerous operating systems and architectures, with
multiple compilers, and using varied compiler flags. The following table lists
the different test case configurations supported

* Operating System: Ubuntu and Microsoft Windows
* Architecture: x64 CPU
* Compiler: gcc, clang, msvc
* Compiler optmization options: O0, O1, O2, O3

Currently, the test programs apply compiler flags focused on optmizations. These
flags often have dramatic, structural effects on generated binaries and can
significantly influence debloating.

## Test Case Naming ##

Test cases are named according to the following scheme: 

`PROGRAM_CPU_OS_COMPILER_OPTIMIZATION`

For example, the following executable is a test case for SQLite3 for a 64bit
processor running linux compiled with GCC using compiler optimization flag -O2:

`sqlite3_exe_amd64_linux_gcc_o2`

## Test Cases ##

**Test**|**Build Instructions**|**Existing Tests**|**Notes**
:-----|:-----|:-----|:-----
Sqlite| [Build Instructions](https://github.com/sqlite/sqlite/blob/ab7fdca2eec1b6d5143214155aa9dfda40de1b83/README.md) | SQLite3 tests are located [here](https://github.com/sqlite/sqlite/tree/ab7fdca2eec1b6d5143214155aa9dfda40de1b83/test) | SQL lite is a configurable database interface.
tar| [Build Instructions](https://github.com/tpcp-project/tar/blob/e50547e1826ec5f8ced2e67bb642009430a45228/INSTALL)| Tar test cases are located [here](https://github.com/SEI-TPCP/DebloatingTestSuiteJSG/tree/master/tar-1.32/tests)| basic, self-contained tar utility. 
coreutils| [Build Instructions](https://github.com/tpcp-project/coreutils/blob/8e81d44b528b0abf6b9f02a70baf47aee52e2930/README-release) |Coreutils tests are [here](https://github.com/tpcp-project/coreutils/tree/8e81d44b528b0abf6b9f02a70baf47aee52e2930/tests),organized by individual utilities | Standard GNU coreutiles library.
Poppler| [Build Instructions](https://github.com/tpcp-project/poppler/blob/39baa7d42966ebd67c2ac91ef1c1450965c37e87/INSTALL) | Poppler tests are [here](https://github.com/tpcp-project/poppler/tree/39baa7d42966ebd67c2ac91ef1c1450965c37e87/test). Specifically, the pdf-inspector utility should be used to examine debloated artifacts. | PDF library for various architectures.
TinyPE|[Repo](https://github.com/pts/pts-tinype). None. TinyPE is already a binary. | None.  | TinyPE is the smallest valid Windows PE file possible.
Tiny-elf|[Repo](https://github.com/tpcp-project/tiny-elf.git). | `nasm -f bin -o a.out tiny.asm` | | TinyPE is the smallest valid Unix ELF file possible.

All releases are in the [TEST_EXECUTABLES](/TEST_EXECUTABLES) directory.
