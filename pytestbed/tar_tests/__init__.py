
from pytestbed.TpcpUnitTest import TpcpTestCase, TpcpTestSuite
import unittest

# TODO: is there a way to automatically import scenario classes?

#from tar_tests.TestTarScenario01Task01 import TestTarScenario01Task01
#from tar_tests.TestTarScenario01Task02 import TestTarScenario01Task02
#from tar_tests.TestTarScenario01Task03 import TestTarScenario01Task03
#from tar_tests.TestTarScenario01Task04 import TestTarScenario01Task04
#from tar_tests.TestTarScenario01Task05 import TestTarScenario01Task05

def load_tests(path):
    suite = TpcpTestSuite(path)
    return suite



