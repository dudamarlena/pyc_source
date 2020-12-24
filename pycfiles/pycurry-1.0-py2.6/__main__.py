# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycurry\test\__main__.py
# Compiled at: 2009-10-25 06:18:23
"""Aggregation of all pycurry module tests.

Copyright (c) 2008 Fons Dijkstra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import unittest, pycurry.dbc as dbc
dbc.level.set(dbc.level.max())
import pycurry as pyc, pycurry.log as log, pycurry.err as err, pycurry.thd as thd, pycurry.tst as tst, pycurry.gof as gof, pycurry.test, pycurry.test.dbc, pycurry.test.log, pycurry.test.err, pycurry.test.thd, pycurry.test.tst, pycurry.test.gof
tst.main(unittest.TestSuite([
 pycurry.test.suite(),
 pycurry.test.dbc.suite(),
 pycurry.test.log.suite(),
 pycurry.test.err.suite(),
 pycurry.test.thd.suite(),
 pycurry.test.gof.suite()]), [
 pyc, dbc, log, err, thd, gof], pyc)