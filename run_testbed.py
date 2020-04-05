#!/usr/bin/python3

import unittest
from unittest.signals import registerResult

import time
import sys
import warnings
import os

import argparse

import subprocess

from pytestbed.UnitTest import TpcpTestCase, TpcpTestResult, TpcpTestRunner
from tar_tests import *
import tar_tests

import inspect

def get_loaded_test_classes():
    loaded = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        print(name, obj)
        if inspect.isclass(obj) and obj.__name__.startswith('Test'):
            loaded.append(obj)
            print(name)
    print(loaded)
    return loaded


###
# Process command options and subcommands
###

def process_cmdline():
    version_txt = 'TPCP Testbed Runner Tool v0.2'
    parser = argparse.ArgumentParser(description=version_txt)
    parser.add_argument('--version', action='version', version='run_testbed.py --- '+version_txt)
    
    parser.add_argument('--tar', action='store', dest='tar_path', metavar='PATH', default=argparse.SUPPRESS, help='run tar tests on executable(s) at PATH')
    
    args = parser.parse_args()
    # returns a dict of the args set
    return vars(args)

###
# Next actually run the tests
###

if __name__ == '__main__':
    args = process_cmdline()
        
    for path in [args[key] for key in args if '_path' in key]:
        # run the tool automatically to generate 'debloated' executables
        #subprocess.run(["config['tool']['path']"], capture_output=True)
        # run the tests on the tool results
        suite = unittest.TestSuite()
        unittest.defaultTestLoader.discover('.tar_tests', pattern='TestTarTask*.py', top_level_dir=None)
        for pymodulename in get_loaded_test_classes():
            print(pymodulename)
            for executable in os.listdir(path):
                print(executable)
                suite.addTest(TpcpTestCase.parametrize(pymodulename, exe=executable))
        TpcpTestRunner(verbosity=2).run(suite)
        #unittest.main(testRunner=TpcpTestRunner)
