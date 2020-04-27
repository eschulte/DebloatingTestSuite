
from pytestbed.TpcpUnitTest import TpcpTestCase, TpcpTestSuite
import unittest

# TODO: is there a way to automatically import scenario classes?

from pytestbed.chmod_tests.ScenarioChmodStandard import standardScenario

def load_tests(path):
    suite = standardScenario(path)
    return suite



