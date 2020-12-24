# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\instruction_registry.py
# Compiled at: 2018-10-06 16:22:48
# Size of source mod 2**32: 2972 bytes
from .instructions import Instruction
from collections import namedtuple

class InstructionRegistry(object):
    __doc__ = '\n    Create a Registry based on a different Instruction Baseclass\n    '

    def __init__(self, instructions, _template_cls=None):
        """
        Instruction Template based Registry

        creates a Registry built from Instruction() objects provided with the _template_cls parameter.
        Falls back to instruction.Instructions() by default.

        :param _template_cls: a subclass of instructions.Instruction with the same constructor arguments
        """
        self._template_cls = Instruction if _template_cls is None else _template_cls
        assert issubclass(self._template_cls, Instruction)
        self._instructions, self._instructions_by_opcode, self._instructions_by_name, self._instruction = (None,
                                                                                                           None,
                                                                                                           None,
                                                                                                           None)
        self._reload(instructions)
        self.instruction_marks_basicblock_end = ['JUMP', 'JUMPI'] + [i.name for i in self.by_category['terminate']]

    def _reload(self, instructions):
        self._instructions = [i.clone(_template=self._template_cls) for i in instructions]
        self._instructions_by_opcode = {obj.opcode:obj for obj in self._instructions}
        self._instructions_by_name = {obj.name:obj for obj in self._instructions}
        self._instructions_by_category = {}
        self._instruction = namedtuple('Instruction', self._instructions_by_name.keys())
        for instr in self._instructions:
            self._instructions_by_category.setdefault(instr.category, [])
            self._instructions_by_category[instr.category].append(instr)
            setattr(self._instruction, instr.name, instr)

    def create_instruction(self, name=None, opcode=None):
        if not name is not None:
            assert opcode is not None
            assert not (name is None and opcode is None)
            if name is not None:
                instr = self.by_name.get(name)
            else:
                if opcode is not None:
                    instr = self.by_opcode.get(opcode)
                    if not instr:
                        instr = self._template_cls(opcode=opcode, name='UNKNOWN_%s' % hex(opcode), description='Invalid opcode', category='unknown')
                else:
                    raise Exception('name or opcode required')
            return instr.clone()

    @property
    def instruction(self):
        return self._instruction

    @property
    def instructions(self):
        return self._instructions

    @property
    def by_opcode(self):
        return self._instructions_by_opcode

    @property
    def by_name(self):
        return self._instructions_by_name

    @property
    def by_category(self):
        return self._instructions_by_category