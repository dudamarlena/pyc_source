# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/bdgenomics/adam/find_adam_home.py
# Compiled at: 2018-11-13 17:10:55
# Size of source mod 2**32: 2659 bytes
from __future__ import print_function
import os, sys

def _find_adam_home():
    """Find the ADAM_HOME."""
    if 'ADAM_HOME' in os.environ:
        return os.environ['ADAM_HOME']

    def is_adam_home(path):
        """Takes a path and returns true if the provided path could be a reasonable ADAM_HOME"""
        return os.path.isfile(os.path.join(path, 'bin/adam-submit')) and (os.path.isdir(os.path.join(path, 'jars')) or os.path.isdir(os.path.join(path, 'adam-assembly/target')))

    paths = [
     os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')]
    if sys.version < '3':
        import imp
        try:
            module_home = imp.find_module('bdgenomics')[1]
            paths.append(os.path.join(module_home, 'adam'))
        except ImportError:
            pass

    else:
        from importlib.util import find_spec
        try:
            module_home = os.path.dirname(find_spec('bdgenomics').origin)
            paths.append(os.path.join(module_home, 'adam'))
        except ImportError:
            pass

        print((repr(paths)), file=(sys.stderr))
        paths = [os.path.abspath(p) for p in paths]
        try:
            return next((path for path in paths if is_adam_home(path)))
        except StopIteration:
            print(('Could not find valid ADAM_HOME while searching {0}'.format(paths)), file=(sys.stderr))
            exit(1)


if __name__ == '__main__':
    print(_find_adam_home())