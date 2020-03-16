import unittest
import subprocess
import os
import tempfile

from pytestbed.UnitTest import TpcpTestCase

class TestTarScenario1(TpcpTestCase):
    
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
            
    def test_1(self):
        with tempfile.TemporaryDirectory() as directory:
            #print('The created temporary directory is %s' % directory)
            # copy files to temp dir
            subprocess.run(["cp", "./"+self._workdir+"filetest.tar", directory])
            subprocess.run(["cp", "./"+self._workdir+"exes/"+self.exe, directory])
            # run commands in temp dir
            os.chdir(directory)
            subprocess.run(["./"+self.exe,"--extract","--file=filetest.tar"])
            output = subprocess.run(["cat","file1.txt","file2.txt"], capture_output=True)
            self.assertEqual(output.stdout, b'hello \nworld \n')
            
    def test_2(self):
        with tempfile.TemporaryDirectory() as directory:
            #print('The created temporary directory is %s' % directory)
            # copy files to temp dir
            subprocess.run(["cp", "./"+self._workdir+"filetest.tar", directory])
            subprocess.run(["cp", "./"+self._workdir+"exes/"+self.exe, directory])
            # run commands in temp dir
            os.chdir(directory)
            subprocess.run(["./"+self.exe,"--get","--file=filetest.tar"])
            output = subprocess.run(["cat","file1.txt","file2.txt"], capture_output=True)
            self.assertEqual(output.stdout, b'hello \nworld \n')
