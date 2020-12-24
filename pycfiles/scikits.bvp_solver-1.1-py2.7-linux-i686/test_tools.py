# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scikits/bvp_solver/tests/test_tools.py
# Compiled at: 2011-07-22 15:26:36
"""
Created on Aug 20, 2009

@author: johnsalvatier
"""
import scikits.bvp_solver.tools as tools, numpy, nose.tools
from numpy.testing import assert_almost_equal

def test_preparg():
    y = numpy.array([1, 2, 3])
    z = [-numpy.NaN, 1, 2, 3]
    w = [1, 2, 3]
    m = [1, 2, 4, w]
    nose.tools.assert_raises(ValueError, tools.preparg, z)
    nose.tools.assert_raises(ValueError, tools.preparg, m)
    assert_almost_equal(tools.preparg(y), y)
    assert_almost_equal(tools.preparg(w), y)


def test_argShapeTest():
    a = 'sdf'
    b = numpy.array([numpy.Inf, 1, 2, 3])
    c = numpy.array([[1],
     [
      2],
     [
      3]])

    def error1():
        tools.argShapeTest(a, (1, 1), 'sd', 'sd')

    def error2():
        tools.argShapeTest(b, (1, 1), 'sd', 'sd')

    def error3():
        tools.argShapeTest(c, (1, 5), 'sd', 'sd')

    nose.tools.assert_raises(ValueError, tools.argShapeTest, a, (1, 1))
    nose.tools.assert_raises(ValueError, tools.argShapeTest, b, (1, 1))
    nose.tools.assert_raises(ValueError, tools.argShapeTest, c, (1, 5))