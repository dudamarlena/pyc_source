# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/interpreter/interpreter.py
# Compiled at: 2017-11-15 12:24:18
# Size of source mod 2**32: 3311 bytes
from .exceptions import InterpreterStopException, InvalidCodeException, BaseInterpreterError
from .instruction import Instruction
from .state import State

class Interpreter(object):

    def __init__(self, code, state_kwargs=None):
        self._code = code
        self._instructions = []
        self._load_code()
        self._state_kwargs = state_kwargs
        self._active = True

    def _load_code(self):
        started = False
        if not self._code.strip():
            raise InvalidCodeException('Empty code')
        for i, line in enumerate(self._code.splitlines(), start=1):
            line = line.strip().split('#', 1)[0].strip()
            if not not line:
                if line.startswith('#'):
                    pass
                elif line == '.IFJcode17' and not started:
                    started = True
                    continue
                    if not started:
                        raise InvalidCodeException(InvalidCodeException.MISSING_HEADER, line=line, line_index=i)
                    self._instructions.append(Instruction(line=line.strip(), line_index=i))

    def _load_labels(self, state):
        for index, instruction in enumerate(self._instructions):
            if instruction.name == 'LABEL':
                state.labels[instruction.op0.label] = index

    def _prepare_state(self):
        state = State(**self._state_kwargs or {})
        state.program_line = self._instructions[0].line_index if self._instructions else -1
        self._load_labels(state)
        return (
         state, len(self._instructions))

    def run(self):
        state, program_length = self._prepare_state()
        while state.program_counter < program_length and self._active:
            program_counter = state.program_counter
            instruction = self._instructions[state.program_counter]
            try:
                instruction.run(state)
            except InterpreterStopException:
                break

            if program_counter == state.program_counter:
                state.program_counter += 1

        return state

    def debug(self):
        state, program_length = self._prepare_state()
        while state.program_counter < program_length and self._active:
            yield state
            program_counter = state.program_counter
            instruction = self._instructions[state.program_counter]
            try:
                instruction.run(state)
            except InterpreterStopException:
                break

            if program_counter == state.program_counter:
                state.program_counter += 1

        return state

    def program_line(self, program_counter):
        instruction = self._instructions[program_counter]
        return instruction.line_index