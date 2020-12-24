# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/test_decorators.py
# Compiled at: 2011-10-24 17:59:11
from dtest import *
from dtest.policy import ThresholdPolicy
from dtest.strategy import SerialStrategy, UnlimitedParallelStrategy, LimitedParallelStrategy
from dtest.test import DTestFixture
from dtest.util import *

class TestThrowaway(DTestCase):

    def test_fordep(self):
        pass


@skip
def test_skip():
    pass


@failing
def test_failing():
    assert False


@attr(attr1=1, attr2=2)
def test_attr():
    pass


@depends(test_skip, test_attr, TestThrowaway.test_fordep)
def test_depends():
    pass


class DecoratorTestException(Exception):
    pass


@raises(DecoratorTestException)
def test_raises():
    raise DecoratorTestException()


@timed(1)
def test_timed():
    pass


@repeat(2)
def test_repeat():
    pass


@parallel
def test_parallel():
    pass


@parallel(2)
def test_parallel_limited():
    pass


@threshold(50)
def test_threshold():
    pass


class ObjTest(object):
    pass


class ResourceTest(Resource):

    def setUp(self):
        t = ObjTest()
        t.test = True
        return t


@require(test=ResourceTest())
def test_require(test):
    assert_true(test.test)


class TestDecorators(DTestCase):

    @depends(test_timed)
    @classmethod
    def setUpClass(cls):
        pass

    @istest
    def skip(self):
        assert_true(test_skip._dt_dtest.skip)
        assert_false(test_failing._dt_dtest.skip)

    @istest
    def failing(self):
        assert_true(test_failing._dt_dtest.failing)
        assert_false(test_skip._dt_dtest.failing)

    @istest
    def attr(self):
        assert_equal(test_attr._dt_dtest.attr1, 1)
        assert_equal(test_attr._dt_dtest.attr2, 2)

    @istest
    def depends(self):
        assert_in(test_skip._dt_dtest, test_depends._dt_dtest.dependencies)
        assert_in(test_attr._dt_dtest, test_depends._dt_dtest.dependencies)
        assert_in(TestThrowaway.test_fordep._dt_dtest, test_depends._dt_dtest.dependencies)
        assert_in(test_depends._dt_dtest, test_skip._dt_dtest.dependents)
        assert_in(test_depends._dt_dtest, test_attr._dt_dtest.dependents)
        assert_in(test_depends._dt_dtest, TestThrowaway.test_fordep._dt_dtest.dependents)

    @istest
    def raises(self):
        assert_set_equal(test_raises._dt_dtest.raises, set([DecoratorTestException]))
        assert_set_equal(test_timed._dt_dtest.raises, set())

    @istest
    def timed(self):
        assert_equal(test_timed._dt_dtest.timeout, 1)
        assert_is_none(test_raises._dt_dtest.timeout)

    @istest
    def repeat(self):
        assert_equal(test_repeat._dt_dtest.repeat, 2)
        assert_equal(test_timed._dt_dtest.repeat, 1)

    @istest
    def parallel(self):
        assert_is_instance(test_parallel._dt_dtest._strategy, UnlimitedParallelStrategy)
        assert_is_instance(test_timed._dt_dtest._strategy, SerialStrategy)

    @istest
    def parallel_limited(self):
        assert_is_instance(test_parallel_limited._dt_dtest._strategy, LimitedParallelStrategy)
        assert_equal(test_parallel_limited._dt_dtest._strategy.limit, 2)

    @istest
    def threshold(self):
        assert_is_instance(test_threshold._dt_dtest._policy, ThresholdPolicy)
        assert_almost_equal(test_threshold._dt_dtest._policy.threshold, 50.0)

    @istest
    def isfixture(self):
        assert_is_instance(self.setUpClass._dt_dtest, DTestFixture)
        assert_in(test_timed._dt_dtest, self.setUpClass._dt_dtest.dependencies)
        assert_in(self.setUpClass._dt_dtest, test_timed._dt_dtest.dependents)

    @istest
    def require(self):
        assert_is_instance(test_require._dt_dtest._resources, dict)
        assert_equal(len(test_require._dt_dtest._resources), 1)
        assert_in('test', test_require._dt_dtest._resources)
        assert_is_instance(test_require._dt_dtest._resources['test'], ResourceTest)
        assert_equal(test_threshold._dt_dtest._resources, {})