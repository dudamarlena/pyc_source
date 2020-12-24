# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/linseed/test/testsuite.py
# Compiled at: 2012-02-12 09:10:21
import unittest

def run():
    suite = unittest.TestLoader().discover(start_dir='.', pattern='*_test.py')
    unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    run()