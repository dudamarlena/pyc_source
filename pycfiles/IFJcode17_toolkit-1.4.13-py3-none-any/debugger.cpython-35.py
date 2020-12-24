# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/interpreter/debugger.py
# Compiled at: 2017-11-08 17:12:51
# Size of source mod 2**32: 2221 bytes
from typing import Set
from .state import State
from .interpreter import Interpreter

class Debugger(object):

    def __init__(self, state_kwargs=None):
        self._breakpoints = set()
        self._interpreter = None
        self._state = None
        self._active = False
        self._state_kwargs = state_kwargs
        self._debugger_iterator = None

    def _start(self, code):
        self._interpreter = Interpreter(code=code, state_kwargs=self._state_kwargs)
        self._active = True

    def add_breakpoint(self, line):
        self._breakpoints.add(line)

    def remove_breakpoint(self, line):
        self._breakpoints.remove(line)

    def run(self, code):
        self._start(code)
        self._state = self._interpreter.run()

    def debug(self, code, breakpoints=None):
        self._start(code)
        self._breakpoints = set(breakpoints) if breakpoints else set()
        self._debugger_iterator = self._interpreter.debug()
        return self.run_to_next_breakpoint()

    def stop(self):
        self._active = False
        self._state = self._debugger_iterator = None
        if self._interpreter:
            self._interpreter._active = False

    def run_to_next_breakpoint(self):
        if not self._active:
            raise RuntimeError()
        for state in self._debugger_iterator:
            self._state = state
            if not self._active:
                return
            if self._interpreter.program_line(self._state.program_counter) in self._breakpoints:
                return self._state

        self._active = False

    def run_to_next_line(self):
        if not self._active:
            raise RuntimeError()
        try:
            self._state = next(self._debugger_iterator)
        except StopIteration:
            self._active = None
            return

        return self._state

    @property
    def breakpoints(self) -> Set[int]:
        return self._breakpoints

    @breakpoints.setter
    def breakpoints(self, v: Set[int]) -> None:
        self._breakpoints = v