# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\dfa.py
# Compiled at: 2018-02-04 13:45:08
# Size of source mod 2**32: 6115 bytes
__doc__ = '\nPython Lexical Analyser\n\nConverting NFA to DFA\n'
import six
from plex import machines
from plex.machines import LOWEST_PRIORITY
from plex.transitions import TransitionMap

def nfa_to_dfa(old_machine, debug=None):
    """
    Given a nondeterministic Machine, return a new equivalent
    Machine which is deterministic.
    """
    new_machine = machines.FastMachine()
    state_map = StateMap(new_machine)
    for key, old_state in list(old_machine.initial_states.items()):
        new_state = state_map.old_to_new(epsilon_closure(old_state))
        new_machine.make_initial_state(key, new_state)

    for new_state in new_machine.states:
        transitions = TransitionMap()
        for old_state in list(state_map.new_to_old(new_state).keys()):
            for event, old_target_states in list(old_state.transitions.items()):
                if event and old_target_states:
                    transitions.add_set(event, set_epsilon_closure(old_target_states))

        for event, old_states in list(transitions.items()):
            new_machine.add_transitions(new_state, event, state_map.old_to_new(old_states))

    if debug:
        debug.write('\n===== State Mapping =====\n')
        state_map.dump(debug)
    return new_machine


def set_epsilon_closure(state_set):
    """
    Given a set of states, return the union of the epsilon
    closures of its member states.
    """
    result = {}
    for state1 in list(state_set.keys()):
        for state2 in list(epsilon_closure(state1).keys()):
            result[state2] = 1

    return result


def epsilon_closure(state):
    """
    Return the set of states reachable from the given state
    by epsilon moves.
    """
    result = state.epsilon_closure
    if result is None:
        result = {}
        state.epsilon_closure = result
        add_to_epsilon_closure(result, state)
    return result


def add_to_epsilon_closure(state_set, state):
    """
    Recursively add to |state_set| states reachable from the given state
    by epsilon moves.
    """
    if not state_set.get(state, 0):
        state_set[state] = 1
        state_set_2 = state.transitions.get_epsilon()
        if state_set_2:
            for state2 in list(state_set_2.keys()):
                add_to_epsilon_closure(state_set, state2)


class StateMap:
    """StateMap"""
    new_machine = None
    old_to_new_dict = None
    new_to_old_dict = None

    def __init__(self, new_machine):
        self.new_machine = new_machine
        self.old_to_new_dict = {}
        self.new_to_old_dict = {}

    def old_to_new(self, old_state_set):
        """
        Return the state of the new machine corresponding to the
        set of old machine states represented by |state_set|. A new
        state will be created if necessary. If any of the old states
        are accepting states, the new state will be an accepting state
        with the highest priority action from the old states.
        """
        key = self.make_key(old_state_set)
        new_state = self.old_to_new_dict.get(key, None)
        if not new_state:
            action = self.highest_priority_action(old_state_set)
            new_state = self.new_machine.new_state(action)
            self.old_to_new_dict[key] = new_state
            self.new_to_old_dict[id(new_state)] = old_state_set
        return new_state

    def highest_priority_action(self, state_set):
        best_action = None
        best_priority = LOWEST_PRIORITY
        for state in list(state_set.keys()):
            priority = state.action_priority
            if priority > best_priority:
                best_action = state.action
                best_priority = priority

        return best_action

    def new_to_old(self, new_state):
        """Given a new state, return a set of corresponding old states."""
        return self.new_to_old_dict[id(new_state)]

    def make_key(self, state_set):
        """
        Convert a set of states into a uniquified
        sorted tuple suitable for use as a dictionary key.
        """
        lst = list(state_set.keys())
        if six.PY2:
            lst.sort()
        return tuple(lst)

    def dump(self, file):
        from .transitions import state_set_str
        for new_state in self.new_machine.states:
            old_state_set = self.new_to_old_dict[id(new_state)]
            file.write('   State %s <-- %s\n' % (
             new_state['number'], state_set_str(old_state_set)))