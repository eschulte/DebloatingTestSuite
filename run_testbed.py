#!/usr/bin/python3

import configparser

import unittest
from unittest.signals import registerResult

import time
import sys
import warnings
import os

import argparse

import subprocess

from pytestbed.UnitTest import TpcpTestCase, TpcpTestResult, TpcpTestRunner
from tar_tests.TarTests import TestTarScenario1

###
# store config in an easily editable .ini file.
# Performers would update this to point path at the
# path to their tool command.
#
# see:
# https://docs.python.org/3/library/configparser.html
###
def get_config():
    config = configparser.ConfigParser()

    readlist = config.read('testing.ini')
    if readlist == []:
        config['tool'] = {'path': '/usr/bin/cp'}
        with open('testing.ini', 'w') as configfile:
            config.write(configfile)
            
    return config


###
# Process command options and subcommands
###

def process_cmdline():
    parser = argparse.ArgumentParser(description='TPCP Testbed Runner Tool')
    parser.add_argument('--version', action='version', version='run_testbed v0.1')
    parser.add_argument('--exclude', action='append', help='exclude a specific testcase from the testbed run')
    
    args = parser.parse_args()
    return args

###
# Next actually run the tests
###

if __name__ == '__main__':
    config = get_config()
    # run the tool automatically to generate 'debloated' executables
    #subprocess.run(["config['tool']['path']"], capture_output=True)
    # run the tests on the tool results
    suite = unittest.TestSuite()
    for executable in os.listdir(os.getcwd()+'/tar_tests/exes/'):
        suite.addTest(TpcpTestCase.parametrize(TestTarScenario1, exe=executable))
    TpcpTestRunner(verbosity=2).run(suite)
    #unittest.main(testRunner=TpcpTestRunner)
