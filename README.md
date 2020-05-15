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
executable file (e.g., to run the tests against a single executable of user's
choice).

For example, to run the test suite on a debloated executable of tar,
located at the user's home directory and named `~/tar_debloat`, you could
type:
```python
./run_testbed.py --tar ~/tar_debloat
```
to run only the tar test suite on that specific debloated executable.
It is up to the user to run any debloating and/or analysis tools on a given
executable *first* before running the test suite on the resulting executable.
A collection of standard, unmanipulated executables is provided for
various architectures and compiler options, for each available test suite.

You could run more than one testbed at a time if preferred. Each testbed
gets its own path to executables.

For more info on which test suites are available, check the help:
```python
./run_testbed.py -h
```

## Test Suite Standard Executables ##

Each test suite comes with a directory of standard executables for testing.
These programs are meant to provide a suite of test cases to run debloating
or feature remove utilities on. It is up to the user to run debloating tools
as desired on these standard test programs. Once the programs are debloated,
the resulting debloated executable may be provided to the test suite to
test if the executable behaves as expected.

Each test program is compiled for numerous operating systems and architectures,
with multiple compilers, and using varied compiler flags. The following table
lists the different test case configurations currently supported for programs.
The exact combinations vary depending on the program.

* Operating System: Ubuntu and Microsoft Windows
* Architecture: x64, ARM, PowerPC
* Compiler: gcc, clang, msvc
* Compiler optimization options: O0, O1, O2, O3

Currently, the test programs apply compiler flags focused on optimizations.
These flags often have dramatic, structural effects on generated binaries and
can significantly influence debloating.

Test programs are built automatically using GitHub's Travis CI integration.
Each test suite is represented as a git submodule within this top-level repo.
Each submodule is a link to a TPCP-cloned repo of the suite's source code.
Each submodule also contains a `.travis.yaml` file specifying the build
configurations for the executable, which may or may not include all available
operating system and compiler options; it depends on which are supported
by the original developers and source code. The automatically built executables
appears on the GitHub releases page as build artifacts, that are automatically
retrieve via a python script and added to this git repository.

Researchers are encouraged to add more testing executables to the appropriate
directories in order to reflect more compiler options or other changes.
Ideally, other build configurations will be captured in Travis CI and added
to our .travis.yaml configuration so that it may be built automatically
in the future as needed.

## Test Case Naming And Architecture ##

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

## How to Add Test Cases To Existing Test Suites ##

As described in the previous section, one must subclass `TpcpTestCase` in
order to create a new test case for a given test suite. This test case must
be added to the test suite manually at this time.

You can write it from scratch or use the following template to get started:

```python
import unittest
import subprocess
import os
import tempfile

from pytestbed.TpcpUnitTest import TpcpTestCase

class TestTarExtractFile(TpcpTestCase):
    
    @classmethod
    def setUpClass(cls):
        # save the working directory we were in before running this test
        cls._originaldir = os.getcwd()
        # TODO: update with the name of the test suite
        cls._workdir = 'tar_tests/'
        # create a new temp directory to do our work in
        cls._tmpdir = tempfile.TemporaryDirectory()
        
    @classmethod
    def tearDownClass(cls):
        # restore old working directory
        os.chdir(cls._originaldir)
        # remove the tmpdir
        cls._tmpdir.cleanup()
        
    def setUp(self):
        # reset dir, so we're not stuck in a non-existent temp dir
        os.chdir(self._originaldir)
        
    ### define real tests below!
    
    def runTest(self):
        # TODO: add your testing commands here!
        # you usually start by copying testing files to your temp directory
        subprocess.run(["cp", "./"+self._workdir+"test.tar", self._tmpdir.name])
        # next, switch python command line to the temp working directory
        os.chdir(self._tmpdir.name)
        # finally, run your debloated executable and other necessary set up here
        # you can access the full path to your debloated executable that was
        # passed to the test case by using self.exe, as below:
        subprocess.run([self.exe,"--option1","--option2=test.tar"])
        output = subprocess.run(["cat","file1.txt","file2.txt"], capture_output=True)
        # every test should include at least one instance of
        # assertBehavior and/or assertBoolean (see description below),
        # the simplest check is to check that we got the expected output
        # on the command line, but any unittest options would work.
        self.assertBehavior(output.stdout, b'hello \nworld \n')
```

Note that we define some special unittest functions that are aware of
whether a test is expected to pass or not in a given Scenario.
- `assertBoolean` expects its argument to be `True` if the test case
  is meant to pass in this Scenario, otherwise it expects `False`.
- `assertBehavior` expects its two arguments to be equal if the test
  case is meant to pass in this Scenario, otherwise it expects inequality.

The steps involved to fully add a new test case are:

1. Use the template above to create a `TpcpTestCase`, or write your own.
2. Place this test case in the appropriate test suite, for example, `tar_tests`.
3. Add the test case to all desired Scenarios in the test suite by importing
   your new test case class into the Scenario, then adding a line like:
   `suite.addTest(TestClassNameHere(succeeds=True, exe=path))`, where `succeeds`
   is set to `True` or `False` depending on if the test is expected to pass
   or fail in this Scenario (for example, if the test corresponds with a
   feature expected to be removed).
4. If desired, an entirely new Scenario can be created by creating a new
   function that returns an instance of `TpcpTestSuite`. Individual unit tests
   must be added to the test suite first before returning, similar to the
   `addTest` example given in step 3. If you created a new Scenario, be sure
   you've added it to the `__init__.py` file in the test suite directory!
   
These steps are preliminary and feedback is welcome! In particular,
unit tests being added to the suite automatically is a near future goal.

## Test Suites ##

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
