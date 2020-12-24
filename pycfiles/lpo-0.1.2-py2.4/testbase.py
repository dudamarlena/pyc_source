# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lpo/test/testbase.py
# Compiled at: 2008-07-30 12:52:46
import sys, unittest

def main(suite=None):
    if not suite:
        if len(sys.argv[1:]):
            suite = unittest.TestLoader().loadTestsFromNames(sys.argv[1:], __import__('__main__'))
        else:
            suite = unittest.TestLoader().loadTestsFromModule(__import__('__main__'))
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
    sys.exit(not result.wasSuccessful())