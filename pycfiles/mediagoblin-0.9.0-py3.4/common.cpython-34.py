# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/common.py
# Compiled at: 2014-06-22 22:43:36
# Size of source mod 2**32: 2109 bytes
import sys
TESTS_ENABLED = False

def import_component(import_string):
    """
    Import a module component defined by STRING.  Probably a method,
    class, or global variable.

    Args:
     - import_string: a string that defines what to import.  Written
       in the format of "module1.module2:component"
    """
    module_name, func_name = import_string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func


def simple_printer(string):
    """
    Prints a string, but without an auto 
 at the end.

    Useful for places where we want to dependency inject for printing.
    """
    sys.stdout.write(string)
    sys.stdout.flush()


class CollectingPrinter(object):
    __doc__ = '\n    Another printer object, this one useful for capturing output for\n    examination during testing or otherwise.\n\n    Use this like:\n\n      >>> printer = CollectingPrinter()\n      >>> printer("herp derp\n")\n      >>> printer("lollerskates\n")\n      >>> printer.combined_string\n      "herp derp\nlollerskates\n"\n    '

    def __init__(self):
        self.collection = []

    def __call__(self, string):
        self.collection.append(string)

    @property
    def combined_string(self):
        return ''.join(self.collection)


# global TESTS_ENABLED ## Warning: Unused global