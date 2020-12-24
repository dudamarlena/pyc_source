# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/unit/all.py
# Compiled at: 2009-12-08 17:43:28
"""
Run all tests in the current directory as a single suite.
"""
import glob, imp, os, sys, unittest

def main():
    suite = unittest.TestSuite()
    for filename in glob.glob('test*.py'):
        name = filename[:-3]
        (file, path, desc) = imp.find_module(name)
        tmod = imp.load_module(name, file, path, desc)
        suite.addTest(tmod.suite())

    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return (1, 0)[result.wasSuccessful()]


if __name__ == '__main__':
    workdir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(workdir)
    sys.exit(main())