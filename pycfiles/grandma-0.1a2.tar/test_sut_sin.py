# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/tests/test_sut_sin.py
# Compiled at: 2010-10-28 14:05:19
import unittest, grandma
from nose.tools import ok_, assert_false, assert_almost_equal
from sample_sut_sin import sut_sin
from sample_sut_ziggzagg import sut_ziggzagg
from sample_sut_sin_error import sut_sin_error
from sample_sut_sin_wrong import sut_sin_wrong

def run_constraints(tests, heuristics, env):
    """Run the tests on the SUT using heuristics to verify results."""
    for t in tests:
        for h in heuristics:
            env.update(t)
            result = eval(h, dict(__builtins__=None, True=True, False=False), env)
            ok_(result, '%s failed heuristic "%s"' % (t, h))

    return


def equal(x, y):
    """
    Almost equal helper for floats.
    This is necessary because in Python sin(radians(180)) is not 0.0!
    """
    EPS = 1e-15
    return abs(x - y) < EPS


def test_sut_sample_oracle():
    """
    Use sample oracle to test the SUT.
    """
    assert_almost_equal(sut_sin(0.0), 0.0)
    assert_almost_equal(sut_sin(90.0), 1.0)
    assert_almost_equal(sut_sin(180.0), 0.0)
    assert_almost_equal(sut_sin(270.0), -1.0)
    assert_almost_equal(sut_sin(360.0), 0.0)


def test_sut_heuristic_oracle():
    """
    Use heuristic oracle to test the SUT.
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
    env = {'delta': 0.1, 'sut': sut_sin, 'equal': equal}
    tests = [ {'x': x} for x in xrange(0, 360) ]
    run_constraints(tests, heuristics, env)


def test_sut_ziggzagg():
    """
    Ziggzagg is not a sin() function but undetected by heuristics.
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
    env = {'delta': 0.1, 'sut': sut_ziggzagg, 'equal': equal}
    tests = [ {'x': x} for x in xrange(0, 360) ]
    run_constraints(tests, heuristics, env)


def test_sut_sin_error():
    """
    An erroneous sin() function is detected by heuristics.
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
    env = {'delta': 0.1, 'sut': sut_sin_error, 'equal': equal}
    tests = [ {'x': x} for x in xrange(0, 360) ]
    run_constraints(tests, heuristics, env)


def test_sut_sin_wrong():
    """
    sin() function has wrong slope but undetected by heuristics.
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
    env = {'delta': 0.1, 'sut': sut_sin_wrong, 'equal': equal}
    tests = [ {'x': x} for x in xrange(0, 360) ]
    run_constraints(tests, heuristics, env)