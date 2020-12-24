# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/eggchecker/runtests.py
# Compiled at: 2007-11-29 10:15:53
"""
extracted and adapted from zope testrunner script
"""
import logging, os, sys, warnings

def run_tests(root_directory):
    """launch tests over zope.testrunner"""
    root_directory = os.path.abspath(root_directory)
    sys.path[:] = [ p for p in sys.path if os.path.abspath(p) != root_directory ]
    if root_directory not in sys.path:
        sys.path.insert(0, root_directory)
    from zope.testing import testrunner
    defaults = ['--tests-pattern', '^f?tests$', '--test-path', root_directory]
    warnings.filterwarnings('ignore', 'PyCrypto', RuntimeWarning, 'twisted[.]conch[.]ssh')
    if 'ztest' in sys.argv:
        sys.argv.remove('ztest')
    result = testrunner.run(defaults)
    logging.disable(999999999)
    sys.exit(result)