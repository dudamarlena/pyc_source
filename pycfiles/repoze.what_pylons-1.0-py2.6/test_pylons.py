# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_pylons.py
# Compiled at: 2009-03-16 12:26:13
"""
Tests for this plugin when used in Pylons.

"""
from tests.fixture.pylonsapp import BasicPylonsController, SecurePanel, SecurePanelWithHandler
from base_tests import ActionDecoratorTestCase, ControllerDecoratorTestCase, ControllerDecoratorWithHandlerTestCase, TestWSGIController, EvaluatorsTestCase, TestBooleanizer

class BasePylonsTester(TestWSGIController):
    """Base test case for Pylons controllers"""
    controller = BasicPylonsController


class TestActionDecoratorInPylons(ActionDecoratorTestCase, BasePylonsTester):
    """Test case for @ActionDecoratorTestCase decorator"""
    pass


class TestControllerDecoratorInPylons(ControllerDecoratorTestCase, BasePylonsTester):
    """Test case for @ControllerDecoratorTestCase decorator"""
    controller = SecurePanel


class TestControllerDecoratorWithHandlerInPylons(ControllerDecoratorWithHandlerTestCase, BasePylonsTester):
    """Test case for @ControllerDecoratorTestCase decorator with handler"""
    controller = SecurePanelWithHandler


class TestEvaluatorsInPylons(EvaluatorsTestCase, BasePylonsTester):
    """Test case for predicate evaluators"""
    pass


class TestBooleanizerInPylons(TestBooleanizer, BasePylonsTester):
    """Test case for the predicate booleanizer"""

    def tearDown(self):
        TestBooleanizer.tearDown(self)
        BasePylonsTester.tearDown(self)