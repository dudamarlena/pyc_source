# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/__init__.py
# Compiled at: 2019-02-24 19:59:56
import unittest, os, sys
test_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(test_dir))

def main():
    runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
    suite = unittest.TestLoader().discover(test_dir, pattern='*test.py')
    raise SystemExit(not runner.run(suite).wasSuccessful())


if __name__ == '__main__':
    main()