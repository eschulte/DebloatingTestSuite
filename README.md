# TPCP Debloating Test Suite #

This repository contains test programs for TPCP. The test programs are
meant to support the development of debloating tools that analyze
native binaries. The example test cases are selected using a number of
different dimensions, such as size, number of components, and
configurability.

## Quick Start ##

```python
./run_testbed.py [[--TESTNAME PATH] ...]
```
where "TESTNAME" is the name of the executable to test. This name
generally matches the name of the git submodule you wish to test.

Each TESTNAME takes a PATH as an option. The path is a full path to a single
executable file (to run the tests against a single executable of user's
choice).

You could run more than one testbed at a time if preferred. Each testbed
gets its own path to executables.

For more info on which options are available, check the help:
```python
./run_testbed.py -h
```

## Test Program Options ##

Each test program is compiled for numerous operating systems and architectures,
with multiple compilers, and using varied compiler flags. The following table
lists the different test case configurations supported

* Operating System: Ubuntu and Microsoft Windows
* Architecture: x64, ARM, PowerPC
* Compiler: gcc, clang, msvc
* Compiler optimization options: O0, O1, O2, O3

Currently, the test programs apply compiler flags focused on optimizations.
These flags often have dramatic, structural effects on generated binaries and
can significantly influence debloating.

## Test Case Naming And Architecture ##

Each test case project is listed as a git submodule that links to its own cloned
repository. Each submodule's cloned repository contains additional Travis CI
and/or cmake build configuration information to produce executables for
the various operating systems, architectures, etc., listed in the previous
section.

Most of the python logic is in the `pytestbed` directory.
A number of specialized subclasses of `unittest` standard classes are included,
and all begin with `Tpcp` prefix.

The actual test cases are stored in a subdirectory of `pytestbed` based
on the name of the submodule by appending "_tests" to the submodule name.
For example `tar` submodule has a related `tar_tests` directory that contains
all of the debloating tests for tar.

Within each `_tests` directory, there is an `exes` subdirectory that contains
a number of pre-built executables from Travis CI as described above.
Users can take the executables in the `exes` subdirectory and apply
debloating tools to produce debloated test cases to run this test suite on.

The unit tests in each `_tests` directory are defined by classes that start
with the word `Test`. These are subclasses of the `Tpcp` test class.
They must be instantiated with two parameters, a "success" toggle that
determines if the test should pass or not (to accomodate tests expected
to fail when an executable is "debloated"), and a path to an executable
to be used for testing. Individual tests are collected into test suites,
which we call "scenarios", that have a pre-set "success" toggle of each
test to describe different "debloating" environments and scenarios.

## Test Cases ##

Below is a table describe some of the test cases we initially looked at.
Not all may have tests within the test suite yet, but are listed here for
discussion purposes as the test suite evolves.

**Test**|**Build Instructions**|**Existing Tests**|**Notes**
:-----|:-----|:-----|:-----
Sqlite| [Build Instructions](https://github.com/sqlite/sqlite/blob/ab7fdca2eec1b6d5143214155aa9dfda40de1b83/README.md) | SQLite3 tests are located [here](https://github.com/sqlite/sqlite/tree/ab7fdca2eec1b6d5143214155aa9dfda40de1b83/test) | SQL lite is a configurable database interface.
tar| [Build Instructions](https://github.com/tpcp-project/tar/blob/e50547e1826ec5f8ced2e67bb642009430a45228/INSTALL)| Tar test cases are located [here](https://github.com/SEI-TPCP/DebloatingTestSuiteJSG/tree/master/tar-1.32/tests)| basic, self-contained tar utility. 
coreutils| [Build Instructions](https://github.com/tpcp-project/coreutils/blob/8e81d44b528b0abf6b9f02a70baf47aee52e2930/README-release) |Coreutils tests are [here](https://github.com/tpcp-project/coreutils/tree/8e81d44b528b0abf6b9f02a70baf47aee52e2930/tests),organized by individual utilities | Standard GNU coreutils library.
Poppler| [Build Instructions](https://github.com/tpcp-project/poppler/blob/39baa7d42966ebd67c2ac91ef1c1450965c37e87/INSTALL) | Poppler tests are [here](https://github.com/tpcp-project/poppler/tree/39baa7d42966ebd67c2ac91ef1c1450965c37e87/test). Specifically, the pdf-inspector utility should be used to examine debloated artifacts. | PDF library for various architectures.
TinyPE|[Repo](https://github.com/pts/pts-tinype). None. TinyPE is already a binary. | None.  | TinyPE is the smallest valid Windows PE file possible.
Tiny-elf|[Repo](https://github.com/tpcp-project/tiny-elf.git). | `nasm -f bin -o a.out tiny.asm` | | TinyPE is the smallest valid Unix ELF file possible.

## Contact ##

Contact the SEI TPCP team at tpcp-contact@sei.cmu.edu.
