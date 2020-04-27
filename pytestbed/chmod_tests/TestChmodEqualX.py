import unittest
import subprocess
import os
import tempfile

from pytestbed.TpcpUnitTest import TpcpTestCase

class TestChmodEqualX(TpcpTestCase):
    
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
    
    # based on 'equal-x.sh' in coreutils/tests/chmod
    def runTest(self):
        # run commands in temp dir
        os.chdir(self._tmpdir.name)
        # create temp file
        old_mask = os.umask(0o005)
        subprocess.run(["touch", "f.test"])
        os.umask(old_mask)
        #subprocess.run(["chmod","640","f.test"])
        output = subprocess.run(["ls", "-l", "f.test"], capture_output=True)
        #print(output.stdout)
        # check variations of =x
        for mode in ["=x", "=xX", "=Xx", "=x,=X", "=X,=x"]:
            old_mask = os.umask(0o005)
            subprocess.run([self.exe,"a=r,"+mode,"f.test"])
            os.umask(old_mask)
            output = subprocess.run(["ls", "-l", "f.test"], capture_output=True)
            #print(output.stdout)
            self.assertBoolean(b'---x--x---' in output.stdout)

            
