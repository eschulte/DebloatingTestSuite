import unittest
import subprocess
import os
import tempfile

from pytestbed.TpcpUnitTest import TpcpTestCase

class TestTarUpdateFile(TpcpTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._originaldir = os.getcwd()
        cls._workdir = 'tar_tests/'
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
    
    # tests replacing of contents of a file inside the archive
    # tar --compare --file=test.tar [FILE]
    def runTest(self):
        # copy files to temp dir
        subprocess.run(["cp", "./"+self._workdir+"test.tar", self._tmpdir.name])
        subprocess.run(["cp", "./"+self._workdir+"file2.txt", self._tmpdir.name])
        subprocess.run(["cat", "This is new file1 text", ">", self._tmpdir.name+"/file1.txt"])
        # run commands in temp dir
        os.chdir(self._tmpdir.name)
        # real test: concat and extract, then cat extracted files to check correct extraction
        output = subprocess.run([self.exe,"--compare","--file=test.tar", "file1.txt"], capture_output=True)
        self.assertBehavior(output.stdout, b'file1.txt: Mod time differs\nfile1.txt: Contents differ\n')
        output = subprocess.run([self.exe,"--compare","--file=test.tar", "file2.txt"], capture_output=True)
        self.assertBehavior(output.stdout, b'\n')

            
