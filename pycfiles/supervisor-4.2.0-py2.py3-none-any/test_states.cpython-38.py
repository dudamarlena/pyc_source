# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/tests/test_states.py
# Compiled at: 2017-07-24 14:57:05
# Size of source mod 2**32: 2277 bytes
"""Test suite for supervisor.states"""
import sys, unittest
from supervisor import states

class TopLevelProcessStateTests(unittest.TestCase):

    def test_module_has_process_states(self):
        self.assertTrue(hasattr(states, 'ProcessStates'))

    def test_stopped_states_do_not_overlap_with_running_states(self):
        for state in states.STOPPED_STATES:
            self.assertFalse(state in states.RUNNING_STATES)

    def test_running_states_do_not_overlap_with_stopped_states(self):
        for state in states.RUNNING_STATES:
            self.assertFalse(state in states.STOPPED_STATES)

    def test_getProcessStateDescription_returns_string_when_found(self):
        state = states.ProcessStates.STARTING
        self.assertEqual(states.getProcessStateDescription(state), 'STARTING')

    def test_getProcessStateDescription_returns_None_when_not_found(self):
        self.assertEqual(states.getProcessStateDescription(3.14159), None)


class TopLevelSupervisorStateTests(unittest.TestCase):

    def test_module_has_supervisor_states(self):
        self.assertTrue(hasattr(states, 'SupervisorStates'))

    def test_getSupervisorStateDescription_returns_string_when_found(self):
        state = states.SupervisorStates.RUNNING
        self.assertEqual(states.getSupervisorStateDescription(state), 'RUNNING')

    def test_getSupervisorStateDescription_returns_None_when_not_found(self):
        self.assertEqual(states.getSupervisorStateDescription(3.14159), None)


class TopLevelEventListenerStateTests(unittest.TestCase):

    def test_module_has_eventlistener_states(self):
        self.assertTrue(hasattr(states, 'EventListenerStates'))

    def test_getEventListenerStateDescription_returns_string_when_found(self):
        state = states.EventListenerStates.ACKNOWLEDGED
        self.assertEqual(states.getEventListenerStateDescription(state), 'ACKNOWLEDGED')

    def test_getEventListenerStateDescription_returns_None_when_not_found(self):
        self.assertEqual(states.getEventListenerStateDescription(3.14159), None)


def test_suite():
    return unittest.findTestCases(sys.modules[__name__])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')