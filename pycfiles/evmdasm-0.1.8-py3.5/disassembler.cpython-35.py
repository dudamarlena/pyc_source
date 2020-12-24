# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\evmdasm\disassembler.py
# Compiled at: 2018-10-20 10:34:57
# Size of source mod 2**32: 9658 bytes
import logging
from . import registry, utils
logger = logging.getLogger(__name__)

class EvmDisassembler(object):

    def __init__(self, debug=False, _registry=None):
        self.errors = []
        self.debug = debug
        self._registry = _registry if _registry is not None else registry.registry

    def disassemble(self, bytecode):
        """ Disassemble evm bytecode to a Instruction objects """
        pc = 0
        previous = None
        if not isinstance(bytecode, EvmBytecode):
            evmbytecode = EvmBytecode(bytecode)
        iter_bytecode = iter(evmbytecode.as_bytes)
        seen_stop = False
        for opcode in iter_bytecode:
            logger.debug(opcode)
            try:
                instruction = self._registry.by_opcode[opcode].consume(iter_bytecode)
                if not len(instruction.operand_bytes) == instruction.length_of_operand:
                    logger.error('invalid instruction: %s' % instruction.name)
                    instruction._name = 'INVALID_%s' % hex(opcode)
                    instruction._description = 'Invalid operand'
                    instruction._category = 'unknown'
            except KeyError as ke:
                instruction = self._registry._template_cls(opcode=opcode, name='UNKNOWN_%s' % hex(opcode), description='Invalid opcode', category='unknown')
                if not seen_stop:
                    msg = 'error: byte at address %d (%s) is not a valid operator' % (pc, hex(opcode))
                    if self.debug:
                        logger.exception(msg)
                    self.errors.append('%s; %r' % (msg, ke))

            if instruction.name == 'STOP' and not seen_stop:
                seen_stop = True
            instruction.address = pc
            pc += instruction.size
            instruction.previous = previous
            if previous:
                previous.next = instruction
            previous = instruction
            logger.debug('%s: %s %s' % (hex(instruction.address), instruction.name, instruction.operand))
            yield instruction

    def assemble(self, instructions):
        """ Assemble a list of Instruction() objects to evm bytecode"""
        for instruction in instructions:
            yield instruction.serialize()


class EvmBytecode(object):

    def __init__(self, bytecode):
        self.bytecode = EvmBytecode.normalize_bytecode(bytecode)
        self.errors = []

    def __str__(self):
        return '0x%s' % self.as_hexstring

    @staticmethod
    def normalize_bytecode(bytecode):
        if isinstance(bytecode, bytes):
            return utils.bytes_to_str(bytecode, prefix='')
        if isinstance(bytecode, str):
            bytecode = utils.strip_0x_prefix(bytecode.strip())
            if utils.is_hexstring(bytecode):
                pass
            return bytecode
        raise Exception('invalid input format. hexstring (0x<hexstr>) or bytes accepted. %r' % bytecode)

    def disassemble(self):
        disassembler = EvmDisassembler()
        self.instructions = EvmInstructions(list(disassembler.disassemble(self.as_bytes)))
        self.errors = disassembler.errors
        return self.instructions

    @property
    def as_hexstring(self):
        return self.bytecode

    @property
    def as_bytes(self):
        return utils.str_to_bytes(self.bytecode)


class EvmInstructions(list):

    def __init__(self, instructions, fix_addresses=True):
        super().__init__(instructions)
        self._fix_addresses = fix_addresses
        self._fix_addresses_at_index = 0
        self._fix_addresses_required = False
        self.errors = []

    def __iter__(self):
        self._update_instruction_addresses(at_index=self._fix_addresses_at_index)
        return super().__iter__()

    def __getitem__(self, index):
        if isinstance(index, int):
            stop = index
        else:
            if isinstance(index, slice):
                stop = index.stop
            else:
                raise TypeError('index must be int or slice')
        if stop >= self._fix_addresses_at_index:
            self._update_instruction_addresses(at_index=self._fix_addresses_at_index)
        return super().__getitem__(index)

    def pop(self, *args, **kwargs):
        self._update_instruction_addresses(at_index=self._fix_addresses_at_index)
        return super().pop(*args, **kwargs)

    def __delitem__(self, i):
        self._fix_addresses_required = True
        self._fix_addresses_at_index = min(self._fix_addresses_at_index, i if i >= 0 else (len(self) - i) % len(self))
        return super().__delitem__(i)

    def assemble(self):
        assembler = EvmDisassembler()
        self.bytecode = EvmBytecode(''.join(assembler.assemble(self)))
        self.errors = assembler.errors
        return self.bytecode

    def insert(self, index, obj):
        obj.previous = super().__getitem__(index).previous
        super().__getitem__(index).previous = obj
        obj.next = super().__getitem__(index)
        ret = super().insert(index, obj)
        self._fix_addresses_required = True
        self._fix_addresses_at_index = min(self._fix_addresses_at_index, index if index >= 0 else (len(self) - index) % len(self))
        return ret

    def append(self, obj):
        obj.next = None
        obj.previous = super().__getitem__(-1)
        super().__getitem__(-1).next = obj
        ret = super().append(obj)
        self._fix_addresses_required = True
        self._fix_addresses_at_index = min(self._fix_addresses_at_index, len(self) - 1)
        return ret

    def extend(self, iterable):
        current_length = len(self)
        prevs_item = super().__getitem__(-1) if current_length else None
        for obj in iterable:
            obj.next = None
            obj.previous = prevs_item
            prevs_item = obj

        ret = super().extend(iterable)
        self._fix_addresses_required = True
        self._fix_addresses_at_index = min(self._fix_addresses_at_index, current_length - 1)
        return ret

    def _update_instruction_addresses(self, at_index=0):
        if not self._fix_addresses or not self._fix_addresses_required or len(self) <= 0:
            return
        assert at_index >= 0
        next_pc = 0
        if at_index == 0:
            for instr in super().__iter__():
                instr.address = next_pc
                next_pc += len(instr)

        elif at_index > 0:
            items = iter(super().__getitem__(slice(at_index - 1, None)))
            first_item = next(items)
            next_pc = first_item.address + len(first_item)
            for instr in items:
                instr.address = next_pc
                next_pc += len(instr)

        self._fix_addresses_at_index = len(self) - 1
        self._fix_addresses_required = False

    def get_stack_balance(self):
        depth = 0
        for instr in super().__iter__():
            depth -= instr.pops
            depth += instr.pushes

        return depth

    def get_gas_required(self):
        return sum([i.gas for i in super().__iter__()])

    @property
    def as_string(self):
        return '\n'.join('%s %s' % (i.name, i.operand) for i in super().__iter__())


class EvmProgram(object):
    __doc__ = '\n\n    p = EvmProgram()\n    p.push("abcdefg")\n    c.call(arg1, arg2, arg3, ...)\n    c.op("JUMPDEST")\n\n    # allow chaining\n    c.op("OR").op("OR")\n\n    '

    def __init__(self, _registry=None):
        self._registry = _registry if _registry is not None else registry.registry
        self._program = EvmInstructions()

    def __getattr__(self, item):
        instr = self._registry.by_name.get(item.upper())
        if not instr:
            raise AttributeError('Instruction %s does not exist' % item)

        def callback(*args, **kwargs):
            new_instr = instr.clone()
            assert not kwargs
            assert len(args) <= new_instr.args
            for arg in args:
                self._program.append(self.create_push_for_data(arg))

            self._program.append(new_instr)
            return self

        return callback

    def op(self, name):
        self._program.append(self._registry.create_instruction(name.upper()))
        return self

    def create_push_for_data(self, data):
        if isinstance(data, int):
            data = utils.int2bytes(data)
        instr = self._registry.create_instruction('PUSH%d' % len(data))
        instr.operand_bytes = data
        return instr

    def assemble(self):
        return self._program.assemble()