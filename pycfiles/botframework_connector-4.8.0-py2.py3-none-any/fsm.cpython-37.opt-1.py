# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /botfly/fsm.py
# Compiled at: 2019-12-01 19:13:58
# Size of source mod 2**32: 2699 bytes
__doc__ = '\nBasic FSM for building CLI parsers for prompt expansions, etc.\n'
ANY = -1

class FSMError(Exception):
    pass


class FSM:
    ANY = ANY

    def __init__(self, initial_state=0):
        self._transitions = {}
        self.default_transition = None
        self.RESET = initial_state
        self.initial_state = self.RESET
        self._reset()

    def _reset(self):
        self.stack = []
        self.current_state = self.initial_state

    def reset(self):
        self._reset()

    def push(self, obj):
        self.stack.append(obj)

    def pop(self):
        return self.stack.pop()

    def add_default_transition(self, action, next_state):
        if action is None and next_state is None:
            self.default_transition = None
        else:
            self.default_transition = (
             action, next_state)

    def add_transition(self, input_symbol, state, action, next_state):
        self._transitions[(input_symbol, state)] = (action, next_state)

    def add_transitions(self, symbols, state, action, next_state):
        for c in symbols:
            self.add_transition(c, state, action, next_state)

    def get_transition(self, input_symbol, state):
        try:
            return self._transitions[(input_symbol, state)]
        except KeyError:
            try:
                return self._transitions[(ANY, state)]
            except KeyError:
                if self.default_transition is not None:
                    return self.default_transition
                raise FSMError('Transition {!r} is undefined.'.format(input_symbol))

    def process(self, input_symbol):
        action, next_state = self.get_transition(input_symbol, self.current_state)
        if action is not None:
            action(input_symbol, self)
        if next_state is not None:
            self.current_state = next_state

    def process_string(self, s):
        for c in s:
            self.process(c)


if __name__ == '__main__':
    pass