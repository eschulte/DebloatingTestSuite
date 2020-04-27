
import cProfile
import pstats

import os

import argparse

from pytestbed.version import __version__
from pytestbed.TpcpUnitTest import TpcpTestCase, TpcpTestSuite, TpcpTestResult, TpcpTestRunner

# TODO: add the test suites below manually as they are created,
# unclear if there's a good way to do this automatically
#import pytestbed.tar_tests
import pytestbed.chmod_tests

import unittest



###
# Process command options and subcommands
###

def process_cmdline():
    version_txt = 'TPCP Testbed Runner Tool - v' + __version__
    parser = argparse.ArgumentParser(description=version_txt)
    parser.add_argument('--version', action='version', version='run_testbed.py --- '+version_txt)
    
    parser.add_argument('--chmod', action='store', dest='chmod_path', metavar='PATH', default=argparse.SUPPRESS, help='run chmod tests on executable(s) at PATH')
    parser.add_argument('--tar', action='store', dest='tar_path', metavar='PATH', default=argparse.SUPPRESS, help='run tar tests on executable(s) at PATH')
    
    args = parser.parse_args()
    # returns a dict of the args set
    return vars(args)

###
# Next actually run the tests
###

def run_testbed():
    args = process_cmdline()
    
    if args == {}:
        print("No arguments provided! Please provide at least one test suite to run.")
        print("Rerun with the -h or --help option to get a list of possible test suites and options.")
        
    for option in [key for key in args if '_path' in key]:
        # set the path then loop through all exes in that path
        path = args[option]
        # set the suite details
        suite = None
        if option == 'chmod_path':
            suite = pytestbed.chmod_tests.load_tests(path)
        elif option == 'tar_path':
            # TODO:
            continue
            suite = pytestbed.tar_tests.load_tests(path)
        else:
            continue
        # run the tool automatically to generate 'debloated' executables
        #subprocess.run(["config['tool']['path']"], capture_output=True)
        #for executable in os.listdir(path):
            #print(executable)
            #suite.addTest(TpcpTestCase.parametrize(pymodulename, exe=executable))
        TpcpTestRunner(verbosity=2).run(suite)
        #unittest.main(testRunner=TpcpTestRunner)
