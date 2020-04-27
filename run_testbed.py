#!/usr/bin/python3

from pytestbed.cmdline import run_testbed

import inspect

def get_loaded_test_classes():
    loaded = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        print(name, obj)
        if inspect.isclass(obj) and obj.__name__.startswith('Test'):
            loaded.append(obj)
            print(name)
    print(loaded)
    return loaded


###
# Next actually run the tests
###

if __name__ == '__main__':
    run_testbed()
