# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/iwasakishuto/Github/portfolio/Kerasy/tests/conftest.py
# Compiled at: 2020-05-09 23:31:35
# Size of source mod 2**32: 407 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, warnings
from kerasy.utils import KerasyImprementationWarning

def pytest_addoption(parser):
    parser.addoption('--kerasy-warnings', choices=['error', 'ignore', 'always', 'default', 'module', 'once'], default='ignore')


def pytest_configure(config):
    action = config.getoption('kerasy_warnings')
    warnings.simplefilter(action, category=KerasyImprementationWarning)