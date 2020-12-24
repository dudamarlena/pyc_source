# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/tests/test_cu_abstract.py
# Compiled at: 2016-03-05 12:27:04
# Size of source mod 2**32: 10402 bytes
"""Test case for abstract control units."""
from unittest.mock import create_autospec, call
from pytest import raises
from modelmachine.cu import AbstractControlUnit, RUNNING, HALTED
from modelmachine.cu import ControlUnit
from modelmachine.memory import RegisterMemory, RandomAccessMemory
from modelmachine.alu import ArithmeticLogicUnit, HALT
BYTE_SIZE = 8
HALF_SIZE = 16
WORD_SIZE = 32
OP_MOVE = 0
OP_LOAD = 0
OP_ADD, OP_SUB = (1, 2)
OP_SMUL, OP_SDIVMOD = (3, 4)
OP_COMP = 5
OP_STORE = 16
OP_ADDR = 17
OP_UMUL, OP_UDIVMOD = (19, 20)
OP_SWAP = 32
OP_RMOVE = 32
OP_RADD, OP_RSUB = (33, 34)
OP_RSMUL, OP_RSDIVMOD = (35, 36)
OP_RCOMP = 37
OP_RUMUL, OP_RUDIVMOD = (51, 52)
OP_STPUSH, OP_STPOP, OP_STDUP, OP_STSWAP = (90, 91, 92, 93)
OP_JUMP = 128
OP_JEQ, OP_JNEQ = (129, 130)
OP_SJL, OP_SJGEQ, OP_SJLEQ, OP_SJG = (131, 132, 133, 134)
OP_UJL, OP_UJGEQ, OP_UJLEQ, OP_UJG = (147, 148, 149, 150)
OP_HALT = 153
ARITHMETIC_OPCODES = {
 OP_ADD, OP_SUB, OP_SMUL, OP_SDIVMOD, OP_UMUL, OP_UDIVMOD}
CONDJUMP_OPCODES = {OP_JEQ, OP_JNEQ,
 OP_SJL, OP_SJGEQ, OP_SJLEQ, OP_SJG,
 OP_UJL, OP_UJGEQ, OP_UJLEQ, OP_UJG}
JUMP_OPCODES = CONDJUMP_OPCODES | {OP_JUMP}
REGISTER_OPCODES = {OP_RMOVE, OP_RADD, OP_RSUB, OP_RSMUL,
 OP_RSDIVMOD, OP_RCOMP, OP_RUMUL, OP_RUDIVMOD}

class TestAbstractControlUnit:
    __doc__ = 'Test case for abstract control unit.'
    ram = None
    registers = None
    alu = None
    control_unit = None

    def setup(self):
        """Init state."""
        self.ram = create_autospec(RandomAccessMemory, True, True)
        self.registers = create_autospec(RegisterMemory, True, True)
        self.alu = create_autospec(ArithmeticLogicUnit, True, True)
        self.control_unit = AbstractControlUnit(self.registers, self.ram, self.alu, WORD_SIZE)
        assert self.control_unit.operand_size == WORD_SIZE

    def test_get_status(self):
        """Test halt interaction between ALU and CU."""
        self.registers.fetch.return_value = 0
        assert self.control_unit.get_status() == RUNNING
        self.registers.fetch.return_value = HALT
        assert self.control_unit.get_status() == HALTED

    def test_abstract_methods(self):
        """Abstract class."""
        with raises(NotImplementedError):
            self.control_unit.fetch_and_decode()
        with raises(NotImplementedError):
            self.control_unit.load()
        with raises(NotImplementedError):
            self.control_unit.execute()
        with raises(NotImplementedError):
            self.control_unit.write_back()

    def test_step_and_run(self):
        """Test command execution."""

        def do_nothing():
            """Empty function."""
            pass

        self.control_unit.fetch_and_decode = create_autospec(do_nothing)
        self.control_unit.load = create_autospec(do_nothing)
        self.control_unit.execute = create_autospec(do_nothing)
        self.control_unit.write_back = create_autospec(do_nothing)
        self.control_unit.step()
        self.control_unit.fetch_and_decode.assert_called_once_with()
        self.control_unit.load.assert_called_once_with()
        self.control_unit.execute.assert_called_once_with()
        self.control_unit.write_back.assert_called_once_with()
        self.control_unit.get_status = create_autospec(do_nothing)
        self.control_unit.get_status.return_value = HALTED
        self.control_unit.run()
        self.control_unit.get_status.assert_called_with()
        self.control_unit.fetch_and_decode.assert_called_once_with()
        self.control_unit.load.assert_called_once_with()
        self.control_unit.execute.assert_called_once_with()
        self.control_unit.write_back.assert_called_once_with()


class TestControlUnit:
    __doc__ = 'Test case for abstract bordachenkova control unit.'
    ram = None
    registers = None
    alu = None
    control_unit = None
    arithmetic_opcodes = None
    condjump_opcodes = None
    ir_size = 32
    operand_size = WORD_SIZE
    address_size = BYTE_SIZE

    def setup(self):
        """Init state."""
        self.ram = RandomAccessMemory(WORD_SIZE, 256, 'big')
        self.registers = create_autospec(RegisterMemory, True, True)
        self.alu = create_autospec(ArithmeticLogicUnit, True, True)
        self.control_unit = ControlUnit(WORD_SIZE, BYTE_SIZE, self.registers, self.ram, self.alu, WORD_SIZE)
        self.test_const()

    def test_const(self):
        """Test internal constants."""
        assert isinstance(self.control_unit, AbstractControlUnit)
        assert isinstance(self.control_unit, ControlUnit)
        assert self.control_unit.ir_size == self.ir_size
        assert self.control_unit.operand_size == self.operand_size
        assert self.control_unit.address_size == self.address_size
        assert self.control_unit.OPCODE_SIZE == BYTE_SIZE
        assert self.control_unit.OPCODES['move'] == OP_MOVE
        assert self.control_unit.OPCODES['load'] == OP_LOAD
        assert self.control_unit.OPCODES['store'] == OP_STORE
        assert self.control_unit.OPCODES['swap'] == OP_SWAP
        assert self.control_unit.OPCODES['add'] == OP_ADD
        assert self.control_unit.OPCODES['sub'] == OP_SUB
        assert self.control_unit.OPCODES['smul'] == OP_SMUL
        assert self.control_unit.OPCODES['sdivmod'] == OP_SDIVMOD
        assert self.control_unit.OPCODES['umul'] == OP_UMUL
        assert self.control_unit.OPCODES['udivmod'] == OP_UDIVMOD
        assert self.control_unit.OPCODES['comp'] == OP_COMP
        assert self.control_unit.OPCODES['stpush'] == OP_STPUSH
        assert self.control_unit.OPCODES['stpop'] == OP_STPOP
        assert self.control_unit.OPCODES['stdup'] == OP_STDUP
        assert self.control_unit.OPCODES['stswap'] == OP_STSWAP
        assert self.control_unit.OPCODES['jump'] == OP_JUMP
        assert self.control_unit.OPCODES['jeq'] == OP_JEQ
        assert self.control_unit.OPCODES['jneq'] == OP_JNEQ
        assert self.control_unit.OPCODES['sjl'] == OP_SJL
        assert self.control_unit.OPCODES['sjgeq'] == OP_SJGEQ
        assert self.control_unit.OPCODES['sjleq'] == OP_SJLEQ
        assert self.control_unit.OPCODES['sjg'] == OP_SJG
        assert self.control_unit.OPCODES['ujl'] == OP_UJL
        assert self.control_unit.OPCODES['ujgeq'] == OP_UJGEQ
        assert self.control_unit.OPCODES['ujleq'] == OP_UJLEQ
        assert self.control_unit.OPCODES['ujg'] == OP_UJG
        assert self.control_unit.OPCODES['halt'] == OP_HALT

    def test_fetch_and_decode(self):
        """Abstract class."""
        with raises(NotImplementedError):
            self.control_unit.fetch_and_decode()

    def test_load(self):
        """Abstract class."""
        with raises(NotImplementedError):
            self.control_unit.load()

    def test_write_back(self):
        """Abstract class."""
        with raises(NotImplementedError):
            self.control_unit.write_back()

    def run_fetch(self, value, opcode, instruction_size, and_decode=True, address_size=BYTE_SIZE, ir_size=WORD_SIZE):
        """Run one fetch test."""
        address = 10
        self.ram.put(address, value, instruction_size)
        increment = instruction_size // self.ram.word_size
        self.registers.fetch.reset_mock()
        self.registers.put.reset_mock()

        def get_register(name, size):
            """Get PC."""
            assert name == 'PC'
            assert size == self.control_unit.address_size
            return address

        self.registers.fetch.side_effect = get_register
        if and_decode:
            self.control_unit.fetch_and_decode()
        else:
            self.control_unit.fetch_instruction(instruction_size)
        self.registers.fetch.assert_any_call('PC', address_size)
        self.registers.put.assert_has_calls([call('RI', value, ir_size),
         call('PC', address + increment, address_size)])
        assert self.control_unit.opcode == opcode

    def test_fetch_instruction(self):
        """Right fetch and decode is a half of business."""
        self.run_fetch(16909060, 1, WORD_SIZE, False)

    def test_basic_execute(self, should_move=True):
        """Test basic operations."""
        self.registers.put.reset_mock()
        self.registers.fetch.reset_mock()
        if should_move is not None:
            self.control_unit.opcode = OP_MOVE
            self.alu.move.reset_mock()
            self.control_unit.execute()
            if should_move:
                self.alu.move.assert_called_once_with()
        else:
            assert not self.alu.move.called
            self.control_unit.opcode = OP_ADD
            self.alu.add.reset_mock()
            self.control_unit.execute()
            self.alu.add.assert_called_once_with()
            self.control_unit.opcode = OP_SUB
            self.alu.sub.reset_mock()
            self.control_unit.execute()
            self.alu.sub.assert_called_once_with()
            self.control_unit.opcode = OP_SMUL
            self.alu.smul.reset_mock()
            self.control_unit.execute()
            self.alu.smul.assert_called_once_with()
            self.control_unit.opcode = OP_UMUL
            self.alu.umul.reset_mock()
            self.control_unit.execute()
            self.alu.umul.assert_called_once_with()
            self.control_unit.opcode = OP_SDIVMOD
            self.alu.sdivmod.reset_mock()
            self.control_unit.execute()
            self.alu.sdivmod.assert_called_once_with()
            self.control_unit.opcode = OP_UDIVMOD
            self.alu.udivmod.reset_mock()
            self.control_unit.execute()
            self.alu.udivmod.assert_called_once_with()
            self.control_unit.opcode = OP_HALT
            self.alu.halt.reset_mock()
            self.control_unit.execute()
            self.alu.halt.assert_called_once_with()
            with raises(ValueError):
                self.control_unit.opcode = 152
                self.control_unit.execute()
            assert not self.registers.fetch.called
            if not not self.registers.put.called:
                raise AssertionError