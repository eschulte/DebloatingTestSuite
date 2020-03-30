import unittest
import subprocess
import os
import tempfile

from pytestbed.UnitTest import TpcpTestCase

class TestTarScenario01Task06(TpcpTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._originaldir = os.getcwd()
        cls._workdir = 'tar_tests/'
        
    @classmethod
    def tearDownClass(cls):
        # restore old working directory
        os.chdir(cls._originaldir)
        
    def setUp(self):
        # reset dir, so we're not stuck in a non-existent temp dir
        os.chdir(self._originaldir)
        
    # define real tests below!
    # Test_06 tar -cvf test.tar test_dir/tar --create --file test_dir
            
    def scenario01_task06(self):
        with tempfile.TemporaryDirectory() as directory:
            #print('The created temporary directory is %s' % directory)
            # copy files to temp dir
            subprocess.run(["cp", "./"+self._workdir+"file1.txt", directory])
            subprocess.run(["cp", "./"+self._workdir+"file2.txt", directory])
            subprocess.run(["cp", "./"+self._workdir+"exes/"+self.exe, directory])
            # run commands in temp dir
            os.chdir(directory)
            subprocess.run(["./"+self.exe,"--compare --file=test.tar [FILE]","create --file test_dir","file1.txt","file2.txt"])
            output = subprocess.run(["cat","file1.txt","file2.txt"], capture_output=True)
            self.assertEqual(output.stdout, b'hello \nworld \n')
            
