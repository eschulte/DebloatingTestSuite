
from pytestbed.TpcpUnitTest import TpcpTestCase, TpcpTestSuite
import unittest

# TODO: is there a way to automatically import scenario classes?

from pytestbed.chmod_tests.TestChmodCOption import TestChmodCOption
from pytestbed.chmod_tests.TestChmodEqualX import TestChmodEqualX

def nocoptionScenario(path):
    suite = TpcpTestSuite()
    suite.addTest(TestChmodCOption(succeeds=False, exe=path))
    suite.addTest(TestChmodEqualX(succeeds=True, exe=path))
    return suite   
