# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/motmot/flytrax/tests.py
# Compiled at: 2009-04-14 12:30:53
import pkg_resources, unittest, traxio

def get_test_suite():
    modules = [
     traxio]
    suites = []
    for module in modules:
        suites.append(module.get_test_suite())

    suite = unittest.TestSuite(suites)
    return suite


def test():
    suite = get_test_suite()
    suite.debug()


if __name__ == '__main__':
    test()