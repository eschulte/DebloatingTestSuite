
import cProfile
import pstats

import argparse

from pytestbed.version import __version__

###
# Process command options and subcommands
###

def process_cmdline():
    version_txt = 'TPCP Testbed Runner Tool - v' + __version__
    parser = argparse.ArgumentParser(description=version_txt)
    parser.add_argument('--version', action='version', version='run_testbed.py --- '+version_txt)
    
    parser.add_argument('--tar', action='store', dest='tar_path', metavar='PATH', default=argparse.SUPPRESS, help='run tar tests on executable(s) at PATH')
    
    args = parser.parse_args()
    # returns a dict of the args set
    return vars(args)

###
# Next actually run the tests
###

def run_testbed():
    args = process_cmdline()
        
    for path in [args[key] for key in args if '_path' in key]:
        # run the tool automatically to generate 'debloated' executables
        #subprocess.run(["config['tool']['path']"], capture_output=True)
        # run the tests on the tool results
        suite = unittest.TestSuite()
        unittest.defaultTestLoader.discover('tar_tests', pattern='TestTarTask*.py', top_level_dir='pytestbed')
        for pymodulename in get_loaded_test_classes():
            print(pymodulename)
            for executable in os.listdir(path):
                print(executable)
                suite.addTest(TpcpTestCase.parametrize(pymodulename, exe=executable))
        TpcpTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromName('pytestbed.tar_tests.TestTarTask01'))
        #unittest.main(testRunner=TpcpTestRunner)
