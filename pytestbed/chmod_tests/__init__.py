
from pytestbed.TpcpUnitTest import TpcpTestCase, TpcpTestSuite
import unittest

# TODO: is there a way to automatically import scenario classes?

from pytestbed.chmod_tests.ScenarioChmodStandard import standardScenario
from pytestbed.chmod_tests.ScenarioChmodNoCOption import nocoptionScenario

def load_tests(path):
    suite = standardScenario(path)
    suite.addTest(nocoptionScenario(path))
    return suite



