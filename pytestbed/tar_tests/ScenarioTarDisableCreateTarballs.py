
from pytestbed.TpcpUnitTest import TpcpTestCase, TpcpTestSuite
import unittest

# TODO: is there a way to automatically import scenario classes?

from pytestbed.tar_tests.TestTarExtractFile import TestTarExtractFile
from pytestbed.tar_tests.TestTarGetFile import TestTarGetFile
from pytestbed.tar_tests.TestTarListFile import TestTarListFile
from pytestbed.tar_tests.TestTarConcatFile import TestTarConcatFile
from pytestbed.tar_tests.TestTarCreateFile import TestTarCreateFile
from pytestbed.tar_tests.TestTarCreateDirFile import TestTarCreateDirFile
from pytestbed.tar_tests.TestTarUpdateFile import TestTarUpdateFile
from pytestbed.tar_tests.TestTarDeleteFile import TestTarDeleteFile
from pytestbed.tar_tests.TestTarCompareFile import TestTarCompareFile

def disableCreatingTarballsScenario(path):
    suite = TpcpTestSuite()
    suite.addTest(TestTarExtractFile(succeeds=True, exe=path))
    suite.addTest(TestTarGetFile(succeeds=True, exe=path))
    suite.addTest(TestTarListFile(succeeds=True, exe=path))
    suite.addTest(TestTarConcatFile(succeeds=False, exe=path))
    suite.addTest(TestTarCreateFile(succeeds=False, exe=path))
    suite.addTest(TestTarCreateDirFile(succeeds=False, exe=path))
    suite.addTest(TestTarUpdateFile(succeeds=False, exe=path))
    suite.addTest(TestTarDeleteFile(succeeds=False, exe=path))
    suite.addTest(TestTarCompareFile(succeeds=True, exe=path))
    return suite 
