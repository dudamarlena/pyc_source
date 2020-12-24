# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/path.py
# Compiled at: 2016-03-06 13:46:07
# Size of source mod 2**32: 852 bytes
import sys

def caller_module(level: int=2,
                  sys=sys):
    """This function is taken from Pyramid Web Framework - ``pyramid.path.caller_module``."""
    module_globals = sys._getframe(level).f_globals
    module_name = module_globals.get('__name__') or '__main__'
    module = sys.modules[module_name]
    return module


def caller_package(level: int=2,
                   caller_module=caller_module):
    """This function is taken from Pyramid Web Framework - ``pyramid.path.caller_package``."""
    module = caller_module(level + 1)
    f = getattr(module, '__file__', '')
    if '__init__.py' in f or '__init__$py' in f:
        return module
    package_name = module.__name__.rsplit('.', 1)[0]
    return sys.modules[package_name]