# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/interpreter/state.py
# Compiled at: 2017-12-06 18:20:58
# Size of source mod 2**32: 9450 bytes
import logging, re
from io import StringIO
from typing import Optional, Union
from ifj2017.interpreter.exceptions import UnknownDataTypeError, StringError, VariableAlreadyDefinedError
from .exceptions import EmptyDataStackError, UndefinedVariableError, UndeclaredVariableError, FrameError, UnknownLabelError, InvalidReturnError, InvalidOperandTypeError
from .operand import Operand, TypeOperand
from .prices import InstructionPrices

class State(object):
    program_counter = 0
    executed_instructions = 0
    program_line = 0

    def __init__(self, stdout=None, stderr=None, stdin=None):
        self.stdout = stdout or StringIO()
        self.stderr = stderr or StringIO()
        self.stdin = stdin or StringIO()
        self.temp_frame = None
        self.frame_stack = []
        self.global_frame = {}
        self.call_stack = []
        self.data_stack = []
        self.labels = {}
        self.instruction_price = 0
        self.operand_price = 0

    @property
    def local_frame(self):
        if not self.frame_stack:
            raise FrameError('Access to non existing local frame.')
        return self.frame_stack[(-1)]

    def frame(self, frame: str):
        return {'TF': lambda : self.temp_frame, 
         'LF': lambda : self.local_frame, 
         'GF': lambda : self.global_frame}.get(frame.upper())()

    def create_frame(self):
        self.temp_frame = {}

    def push_frame(self):
        if self.temp_frame is None:
            raise FrameError('Temp frame to push is undefined.')
        self.frame_stack.append(self.temp_frame.copy())
        self.temp_frame = None

    def pop_frame(self):
        if not self.frame_stack:
            raise FrameError('Non-existing frame to pop.')
        self.temp_frame = self.frame_stack[(-1)]
        self.frame_stack = self.frame_stack[:-1]

    def get_value(self, value: Optional[Operand]) -> Union[(None, int, str, float)]:
        if value is None:
            return
        if not isinstance(value, Operand):
            return value
        if value.type == TypeOperand.CONSTANT:
            self.operand_price += InstructionPrices.OPERAND_CONSTANT
            return value.value
        if value.type == TypeOperand.VARIABLE:
            self.operand_price += InstructionPrices.OPERAND_VARIABLE
            variable_value = self.frame(value.frame)[value.name]
            if variable_value is None:
                raise UndefinedVariableError(value.name, value.frame)
            return variable_value
        raise InvalidOperandTypeError()

    def set_value(self, to, what):
        if to.type != TypeOperand.VARIABLE:
            raise InvalidOperandTypeError()
        frame = self.frame(to.frame)
        if frame is None:
            raise FrameError('Non existing frame {}'.format(to.frame))
        if to.name not in frame and what is not None:
            raise UndeclaredVariableError(to.name, to.frame)
        frame[to.name] = self.get_value(what)
        self.operand_price += InstructionPrices.OPERAND_VARIABLE

    def define_variable(self, variable):
        frame = self.frame(variable.frame)
        if variable.name in frame:
            raise VariableAlreadyDefinedError()
        frame[variable.name] = None
        self.operand_price += InstructionPrices.OPERAND_VARIABLE

    def call(self, op):
        if op.label not in self.labels:
            raise UnknownLabelError(op.label)
        self.call_stack.append(self.program_counter)
        self.program_counter = self.labels.get(op.label)

    def return_(self):
        if not self.call_stack:
            raise InvalidReturnError()
        self.program_counter = self.call_stack[(-1)] + 1
        self.call_stack = self.call_stack[:-1]

    def jump(self, op):
        if op.label not in self.labels:
            raise UnknownLabelError(op.label)
        self.program_counter = self.labels.get(op.label)

    def push_stack(self, op):
        value = self.get_value(op)
        logging.debug('Push {} to stack.'.format(value))
        self.data_stack.append(value)
        self.operand_price += InstructionPrices.OPERAND_STACK

    def pop_stack(self, op=None):
        if not self.data_stack:
            raise EmptyDataStackError()
        value = self.data_stack[(-1)]
        logging.debug('Pop {} from stack.'.format(value))
        if op:
            self.set_value(op, value)
        self.operand_price += InstructionPrices.OPERAND_STACK
        self.data_stack = self.data_stack[:-1]
        return value

    def jump_if(self, op0, op1, op2, positive=True):
        equal = self.get_value(op1) == self.get_value(op2)
        if positive == equal:
            self.jump(op0)

    def set_char(self, where, index, from_):
        changed = self.get_value(where)
        changed[self.get_value(index)] = self.get_value(from_)[0]
        self.set_value(where, changed)

    def get_char(self, target, string, index):
        source = self.get_value(string)
        try:
            self.set_value(target, source[self.get_value(index)])
        except IndexError:
            raise StringError(source, self.get_value(index))

    def str_len(self, target, string):
        return self.set_value(target, len(self.get_value(string)))

    def read(self, to, type_):
        loaded = []
        input_ = self.stdin.readline().strip()
        input_len = len(input_)
        if type_.data_type == Operand.CONSTANT_MAPPING_REVERSE.get(str):
            i = input_[0] == '"'
            while i < input_len and input_[i] != '"':
                loaded.append(input_[i])
                i += 1

            try:
                self.set_value(to, ''.join(loaded))
            except ValueError:
                self.set_value(to, '')

        else:
            if type_.data_type == Operand.CONSTANT_MAPPING_REVERSE.get(int):
                i = 0
                while i < input_len and input_[i].isdecimal():
                    loaded.append(input_[i])
                    i += 1

                try:
                    self.set_value(to, int(''.join(loaded)))
                except ValueError:
                    self.set_value(to, 0)

            else:
                if type_.data_type == Operand.CONSTANT_MAPPING_REVERSE.get(Operand.CONSTANT_MAPPING.get('float')):
                    float_re = re.compile('^(\\d+\\.\\d+)|(\\d+[Ee][+-]?\\d+)|(\\d+)')
                    match = float_re.match(input_)
                    assert match
                    try:
                        self.set_value(to, Operand.CONSTANT_MAPPING.get('float')(match.group(0)))
                    except ValueError:
                        self.set_value(to, 0.0)

                else:
                    if type_.data_type == Operand.CONSTANT_MAPPING_REVERSE.get(bool):
                        bool_re = re.compile('^(true|false)', re.IGNORECASE)
                        match = bool_re.match(input_)
                        if match:
                            self.set_value(to, Operand.BOOL_LITERAL_MAPPING.get(match.group(0).lower()))
                        else:
                            self.set_value(to, False)
                    else:
                        raise UnknownDataTypeError()

    ESCAPE_RE = re.compile('\\\\([0-9]{3})')

    def write(self, op):
        value = self.get_value(op)
        rendered = str(value)
        if isinstance(value, bool):
            rendered = str(value).lower()
        else:
            if isinstance(value, int):
                rendered = '{: d}'.format(value)
            elif isinstance(value, float):
                rendered = '{: g}'.format(value)
        self.stdout.write(rendered)

    def string_to_int_stack(self):
        index = self.pop_stack()
        what = self.pop_stack()
        self.push_stack(ord(what[index]))

    def __str__(self):
        join = ', '.join
        return 'State(TF=({}), LF=({})({}), GF=({}), STACK=[{}], PC={}, EXECUTED={}, PRICE={}({}+{}))'.format(join('{}: {}'.format(k, v) for k, v in self.temp_frame.items()) if self.temp_frame else '-', join('{}: {}'.format(k, v) for k, v in self.local_frame.items()) if self.frame_stack else '-', len(self.frame_stack), join('{}: {}'.format(k, v) for k, v in self.global_frame.items()) if self.global_frame else '-', join(map(str, reversed(self.data_stack))), self.program_counter, self.executed_instructions, self.instruction_price + self.operand_price, self.instruction_price, self.operand_price)

    def program_counter_to_label(self, pc):
        return {v:k for k, v in self.labels.items()}.get(pc) or ''

    @property
    def price(self):
        return self.operand_price + self.instruction_price