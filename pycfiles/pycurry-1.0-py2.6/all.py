# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycurry\test\all.py
# Compiled at: 2009-10-25 06:19:25
import unittest, pycurry.test, pycurry.test.dbc, pycurry.test.log, pycurry.test.err, pycurry.test.thd, pycurry.test.tst, pycurry.test.gof

def suite():
    return unittest.TestSuite([pycurry.test.suite(),
     pycurry.test.dbc.suite(),
     pycurry.test.log.suite(),
     pycurry.test.err.suite(),
     pycurry.test.thd.suite(),
     pycurry.test.tst.suite(),
     pycurry.test.gof.suite()])