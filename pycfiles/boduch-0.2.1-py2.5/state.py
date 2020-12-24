# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/test/state.py
# Compiled at: 2009-08-14 17:29:28
import unittest
from boduch.interface import IStateMachine, IStateTransition
from boduch.state import StateMachine, StateTransition
from boduch.predicate import Equal

class TestState(unittest.TestCase):

    def setUp(self):
        self.test_machine_obj = StateMachine()
        self.test_transition_obj = StateTransition()

    def test_A_machine_interface(self):
        """Testing the StateMachine interface"""
        self.assertTrue(IStateMachine.implementedBy(StateMachine), 'IStateMachine not implemented by StateMachine.')
        self.assertTrue(IStateMachine.providedBy(self.test_machine_obj), 'IStateMachine not provided by StateMachine instance.')

    def test_B_transition_interface(self):
        """Testing the StateTransition interface"""
        self.assertTrue(IStateTransition.implementedBy(StateTransition), 'IStateTransition not implemented by StateTransition.')
        self.assertTrue(IStateTransition.providedBy(self.test_transition_obj), 'IStateTransition not provided by instance.')

    def test_C_machine_add_state(self):
        """Testing the StateMachine.add_state() method"""
        length = len(self.test_machine_obj.allowed_states)
        self.test_machine_obj.add_state('RUNNING')
        self.assertTrue(len(self.test_machine_obj.allowed_states) == length + 1, 'Adding a state to the StateMachine instance failed.')

    def test_D_machine_add_trasition(self):
        """Testing the StateMachine.add_transition() method"""
        length = len(self.test_machine_obj.transitions)
        self.test_machine_obj.add_transition('RUNNING', Equal(1, 1))
        self.assertTrue(len(self.test_machine_obj.transitions) == length + 1, 'Adding a transition to the StateMachine instance failed.')

    def test_E_machine_transition(self):
        """Testing the StateMachine.transition() method"""
        self.test_machine_obj.add_state('RUNNING')
        self.test_machine_obj.add_state('OFF')
        self.test_machine_obj.add_transition('OFF', Equal(1, 1))
        self.test_machine_obj.transition()
        self.assertTrue(self.test_machine_obj.current_state == 'OFF', 'Transitioning the the StateMachine instance failed.')

    def test_F_machine_remove_state(self):
        """Testing the StateMachine.remove_state() method"""
        self.test_machine_obj.add_state('RUNNING')
        length = len(self.test_machine_obj.allowed_states)
        self.test_machine_obj.remove_state('RUNNING')
        self.assertTrue(len(self.test_machine_obj.allowed_states) == length - 1, 'Removing a state from the StateMachine instance failed.')

    def test_G_machine_change_state(self):
        """Testing the StateMachine.change_state() method"""
        self.test_machine_obj.add_state('RUNNING')
        self.test_machine_obj.change_state('RUNNING')
        self.assertTrue(self.test_machine_obj.current_state == 'RUNNING', 'Changing the state of the StateMachine instance failed.')

    def test_H_machine_equal(self):
        """Testing the StateMachine.__eq__() method"""
        self.test_machine_obj.add_state('RUNNING')
        self.test_machine_obj.change_state('RUNNING')
        self.assertTrue(self.test_machine_obj == 'RUNNING', 'The StateMachine instance equal operator failed.')

    def test_I_machine_not_equal(self):
        """Testing the StateMachine.__ne__() method"""
        self.test_machine_obj.add_state('RUNNING')
        self.test_machine_obj.change_state('RUNNING')
        self.assertTrue(self.test_machine_obj != 'OFF', 'The StateMachine instance not equal operator failed.')


SuiteState = unittest.TestLoader().loadTestsFromTestCase(TestState)
__all__ = [
 'TestState', 'SuiteState']