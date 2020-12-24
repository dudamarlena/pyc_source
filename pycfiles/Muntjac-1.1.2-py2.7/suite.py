# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/suite.py
# Compiled at: 2013-04-04 15:36:37
import unittest, muntjac.test.server.suite, muntjac.test.server.component.suite, muntjac.test.server.components.suite, muntjac.test.server.data.suite

def suite():
    suite = unittest.TestSuite([
     muntjac.test.server.suite.suite(),
     muntjac.test.server.component.suite.suite(),
     muntjac.test.server.components.suite.suite(),
     muntjac.test.server.data.suite.suite()])
    return suite


def main():
    unittest.TextTestRunner(verbosity=2).run(suite())


if __name__ == '__main__':
    main()