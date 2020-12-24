# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/testing-software/grandma/tests/test_sin_sut.py
# Compiled at: 2010-10-25 15:47:01
import unittest, grandma
from nose.tools import ok_, assert_false
from sample_sin_sut import sin_sut

def run_constraints(tests, heuristics, env):
    """Run the tests on the SUT using heuristics to verify results."""
    for t in tests:
        for h in heuristics:
            env.update(t)
            result = eval(h, dict(__builtins__=None, True=True, False=False), env)
            ok_(result, '%s failed heuristic %s' % (t, h))

    return


def equal(x, y):
    """Almost equal helper for floats"""
    EPS = 1e-15
    return abs(x - y) < EPS


def test_sin_sut():
    """
    Use heurisitcs to test the SUT.
    Heuristics used:
    o sin(0)   = 0
    o sin(90)  = 1
    o sin(180) = 0
    o sin(270) = -1
    o sin(360) = 0
    o increases from   0 -  90
    o decreases from  90 - 180
    o decreases from 180 - 270
    o increases from 270 - 360
    """
    heuristics = [
     'equal(sut(x),  0.0) if x ==   0.0 else True',
     'equal(sut(x),  1.0) if x ==  90.0 else True',
     'equal(sut(x),  0.0) if x == 180.0 else True',
     'equal(sut(x), -1.0) if x == 270.0 else True',
     'equal(sut(x),  0.0) if x == 360.0 else True',
     'sut(x) < sut(x + delta) if   0 <= x and x + delta <=  90 else True',
     'sut(x) > sut(x + delta) if  90 <= x and x + delta <= 180 else True',
     'sut(x) > sut(x + delta) if 180 <= x and x + delta <= 270 else True',
     'sut(x) < sut(x + delta) if 270 <= x and x + delta <= 360 else True']
    env = {'delta': 0.1, 'sut': sin_sut, 'equal': equal}
    tests = [ {'x': x} for x in xrange(0, 360) ]
    run_constraints(tests, heuristics, env)
    assert False