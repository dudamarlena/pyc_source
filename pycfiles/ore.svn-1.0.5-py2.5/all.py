# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/tests/all.py
# Compiled at: 2008-04-15 01:26:21
import unittest, test_Node, test_File, test_Directory, test_Properties, test_Transaction

def test_suite():
    suite = unittest.TestSuite()
    for mod in [test_Node, test_File, test_Directory, test_Properties, test_Transaction]:
        suite.addTests(mod.test_suite())

    return suite


def main():
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite())


if __name__ == '__main__':
    main()