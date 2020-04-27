import unittest
import subprocess
import os
import tempfile

from pytestbed.TpcpUnitTest import TpcpTestCase

class TestChmodCOption(TpcpTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._originaldir = os.getcwd()
        cls._workdir = 'chmod_tests/'
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
    
    # based on 'c-option.sh' in coreutils/tests/chmod
    def runTest(self):
        # run commands in temp dir
        os.chdir(self._tmpdir.name)
        # create temp file
        subprocess.run(["touch", "f.test"])
        subprocess.run([self.exe,"444","f.test"])
        subprocess.run([self.exe,"u=rwx","f.test"])
        # this command changes permissions from 0744 to 0774
        output = subprocess.run([self.exe,"-c","g=rwx","f.test"], capture_output=True)
        self.assertBehavior(output.stdout, b'mode of \'f.test\' changed from 0744 (rwxr--r--) to 0774 (rwxrwxr--)\n')
        # this command doesn't change permission, so should be no output
        output = subprocess.run([self.exe,"-c","g=rwx","f.test"], capture_output=True)
        self.assertBehavior(output.stdout, b'')
        #print(subprocess.run(["ls","-l","f.test"], capture_output=True))

            
