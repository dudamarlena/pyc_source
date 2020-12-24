# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_tg2.py
# Compiled at: 2009-03-16 12:26:40
"""
Tests for this plugin when used in TurboGears 2.

"""
from tests.fixture.tg2app import BasicTGController, SecurePanel, SecurePanelWithHandler
from base_tests import ActionDecoratorTestCase, ControllerDecoratorTestCase, ControllerDecoratorWithHandlerTestCase, TestWSGIController, EvaluatorsTestCase, TestBooleanizer

class BaseTG2Tester(TestWSGIController):
    """Base test case for TG2 controllers"""
    controller = BasicTGController


class TestActionDecoratorInTG2(ActionDecoratorTestCase, BaseTG2Tester):
    """Test case for @ActionDecoratorTestCase decorator"""
    pass


class TestControllerDecoratorInTG2(ControllerDecoratorTestCase, BaseTG2Tester):
    """Test case for @ControllerDecoratorTestCase decorator"""
    controller = SecurePanel


class TestControllerDecoratorWithHandlerInTG2(ControllerDecoratorWithHandlerTestCase, BaseTG2Tester):
    """Test case for @ControllerDecoratorTestCase decorator"""
    controller = SecurePanelWithHandler


class TestEvaluatorsInTG2(EvaluatorsTestCase, BaseTG2Tester):
    """Test case for predicate evaluators"""
    pass


class TestBooleanizerInTG2(TestBooleanizer, BaseTG2Tester):
    """Test case for the predicate booleanizer"""

    def tearDown(self):
        TestBooleanizer.tearDown(self)
        BaseTG2Tester.tearDown(self)