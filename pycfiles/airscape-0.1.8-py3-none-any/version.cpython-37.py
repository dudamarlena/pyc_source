# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mengwei/workspace/mine/airtest_run/airrun/utils/version.py
# Compiled at: 2020-04-15 05:34:06
# Size of source mod 2**32: 541 bytes
__version__ = '0.0.1'
import os, sys

def get_airtest_version():
    pip_pkg_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    pip_pkg_dir = os.path.abspath(pip_pkg_dir)
    import airtest.utils.version as airtest_version
    return 'airrun {} with [airtest {}] from {} (python {})'.format(__version__, airtest_version, pip_pkg_dir, sys.version[:3])


def show_version():
    sys.stdout.write(get_airtest_version())
    sys.stdout.write(os.linesep)
    sys.exit()