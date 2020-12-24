# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/tests/test_cu_variable.py
# Compiled at: 2016-03-05 12:27:04
# Size of source mod 2**32: 24978 bytes
"""Test case for control unit with variable command length."""
from unittest.mock import call
from pytest import raises
from modelmachine.cu import RUNNING, HALTED
from modelmachine.cu import ControlUnitV
from modelmachine.cu import ControlUnitM
from modelmachine.memory import RegisterMemory, RandomAccessMemory
from modelmachine.alu import ArithmeticLogicUnit
from .test_cu_abstract import BYTE_SIZE, HALF_SIZE, WORD_SIZE, OP_MOVE, OP_ADDR, OP_COMP, OP_SDIVMOD, OP_UDIVMOD, OP_LOAD, OP_STORE, OP_RMOVE, OP_RADD, OP_RSUB, OP_RSMUL, OP_RSDIVMOD, OP_RCOMP, OP_RUMUL, OP_RUDIVMOD, OP_JUMP, OP_HALT, ARITHMETIC_OPCODES, CONDJUMP_OPCODES, JUMP_OPCODES, REGISTER_OPCODES
from .test_cu_fixed import TestControlUnit2 as TBCU2

class TestControlUnitV(TBCU2):
    __doc__ = 'Test case for  Model Machine Variable Control Unit.'

    def setup(self):
        """Init state."""
        super().setup()
        self.ram = RandomAccessMemory(BYTE_SIZE, 256, 'big', is_protected=True)
        self.control_unit = ControlUnitV(WORD_SIZE, BYTE_SIZE, self.registers, self.ram, self.alu, WORD_SIZE)
        assert self.control_unit.opcodes == {0, 1, 2, 3, 4,
         19, 20,
         5,
         128, 129, 130,
         131, 132, 133, 134,
         147, 148, 149, 150,
         153}

    def test_fetch_and_decode(self):
        """Right fetch and decode is a half of business."""
        for opcode in set(range(2 ** BYTE_SIZE)) - self.control_unit.opcodes:
            with raises(ValueError):
                self.run_fetch(opcode, opcode, BYTE_SIZE)

        for opcode in ARITHMETIC_OPCODES | {OP_COMP, OP_MOVE}:
            self.control_unit.address1, self.control_unit.address2 = (None, None)
            self.run_fetch(opcode << 16 | 515, opcode, 24)
            assert self.control_unit.address1 == 2
            if not self.control_unit.address2 == 3:
                raise AssertionError

        for opcode in CONDJUMP_OPCODES | {OP_JUMP}:
            self.control_unit.address1, self.control_unit.address2 = (None, None)
            self.run_fetch(opcode << 8 | 2, opcode, 16)
            assert self.control_unit.address1 == 2
            if not self.control_unit.address2 is None:
                raise AssertionError

        for opcode in {OP_HALT}:
            self.control_unit.address1, self.control_unit.address2 = (None, None)
            self.run_fetch(opcode, opcode, 8)
            assert self.control_unit.address1 is None
            if not self.control_unit.address2 is None:
                raise AssertionError

    def test_load(self):
        """R1 := [A1], R2 := [A2]."""
        addr1, val1 = (5, 123456)
        addr2, val2 = (10, 654321)
        self.ram.put(addr1, val1, WORD_SIZE)
        self.ram.put(addr2, val2, WORD_SIZE)
        self.control_unit.address1 = addr1
        self.control_unit.address2 = addr2
        for opcode in ARITHMETIC_OPCODES | {OP_COMP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_has_calls([call('R1', val1, WORD_SIZE),
             call('R2', val2, WORD_SIZE)])

        for opcode in {OP_MOVE}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('R1', val2, WORD_SIZE)

        for opcode in CONDJUMP_OPCODES | {OP_JUMP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('ADDR', addr1, BYTE_SIZE)

        for opcode in {OP_HALT}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            if not not self.registers.put.called:
                raise AssertionError

    def test_step(self):
        """Test step cycle."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 67596, 3 * BYTE_SIZE)
        self.ram.put(3, 328464, 3 * BYTE_SIZE)
        self.ram.put(6, 34324, 2 * BYTE_SIZE)
        self.ram.put(8, 12, WORD_SIZE)
        self.ram.put(12, 10, WORD_SIZE)
        self.ram.put(16, 20, WORD_SIZE)
        self.ram.put(20, 153, BYTE_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.step()
        assert self.ram.fetch(8, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 3
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(8, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 6
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('PC', BYTE_SIZE) == 20
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('PC', BYTE_SIZE) == 21
        assert self.control_unit.get_status() == HALTED

    def test_run(self):
        """Very simple program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 67596, 3 * BYTE_SIZE)
        self.ram.put(3, 328464, 3 * BYTE_SIZE)
        self.ram.put(6, 34324, 2 * BYTE_SIZE)
        self.ram.put(8, 12, WORD_SIZE)
        self.ram.put(12, 10, WORD_SIZE)
        self.ram.put(16, 20, WORD_SIZE)
        self.ram.put(20, 153, BYTE_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.run()
        assert self.ram.fetch(8, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 21
        assert self.control_unit.get_status() == HALTED

    def test_minimal_run(self):
        """Minimal program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 153, BYTE_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.run()
        assert self.registers.fetch('PC', BYTE_SIZE) == 1
        assert self.control_unit.get_status() == HALTED


class TestControlUnitM(TBCU2):
    __doc__ = 'Test case for Address Modification Model Machine Control Unit.'

    def setup(self):
        """Init state."""
        super().setup()
        self.ram = RandomAccessMemory(HALF_SIZE, 2 ** HALF_SIZE, 'big', is_protected=True)
        self.control_unit = ControlUnitM(WORD_SIZE, HALF_SIZE, self.registers, self.ram, self.alu, WORD_SIZE)
        self.operand_size = WORD_SIZE
        self.address_size = 2 * BYTE_SIZE
        assert self.control_unit.opcodes == {0, 1, 2, 3, 4, 5,
         16, 17, 19, 20,
         32, 33, 34, 35, 36, 37,
         51, 52,
         128, 129, 130,
         131, 132, 133, 134,
         147, 148, 149, 150,
         153}

    def test_const(self):
        super().test_const()
        assert self.control_unit.OPCODES['addr'] == OP_ADDR
        assert self.control_unit.OPCODES['rmove'] == OP_RMOVE
        assert self.control_unit.OPCODES['radd'] == OP_RADD
        assert self.control_unit.OPCODES['rsub'] == OP_RSUB
        assert self.control_unit.OPCODES['rsmul'] == OP_RSMUL
        assert self.control_unit.OPCODES['rsdivmod'] == OP_RSDIVMOD
        assert self.control_unit.OPCODES['rcomp'] == OP_RCOMP
        assert self.control_unit.OPCODES['rumul'] == OP_RUMUL
        assert self.control_unit.OPCODES['rudivmod'] == OP_RUDIVMOD

    def run_fetch(self, value, opcode, instruction_size, r2=True):
        """Run one fetch test."""
        address1 = 10
        address2 = 42
        self.ram.put(address1, value, instruction_size)
        increment = instruction_size // self.ram.word_size
        self.registers.fetch.reset_mock()
        self.registers.put.reset_mock()

        def get_register(name, size):
            """Get PC."""
            if name == 'PC':
                assert size == 2 * BYTE_SIZE
                return address1
            if name == 'R2':
                assert size == WORD_SIZE
                return address2
            raise KeyError()

        self.registers.fetch.side_effect = get_register
        self.control_unit.fetch_and_decode()
        if r2:
            self.registers.fetch.assert_has_calls([call('PC', 2 * BYTE_SIZE),
             call('R2', WORD_SIZE)])
        else:
            self.registers.fetch.assert_any_call('PC', 2 * BYTE_SIZE)
        self.registers.put.assert_has_calls([call('RI', value, WORD_SIZE),
         call('PC', address1 + increment, 2 * BYTE_SIZE)])
        assert self.control_unit.opcode == opcode

    def test_fetch_and_decode(self):
        """Right fetch and decode is a half of business."""
        for opcode in set(range(2 ** BYTE_SIZE)) - self.control_unit.opcodes:
            with raises(ValueError):
                self.run_fetch(opcode << BYTE_SIZE, opcode, 2 * BYTE_SIZE)

        for opcode in ARITHMETIC_OPCODES | JUMP_OPCODES | {OP_COMP, OP_LOAD, OP_ADDR, OP_STORE}:
            self.control_unit.register1 = None
            self.control_unit.register2 = None
            self.control_unit.address = None
            self.run_fetch(opcode << 24 | 1179668, opcode, 32)
            assert self.control_unit.register1 == 'R1'
            assert self.control_unit.register2 is None
            if not self.control_unit.address == 62:
                raise AssertionError

        for opcode in REGISTER_OPCODES:
            self.control_unit.register1 = None
            self.control_unit.register2 = None
            self.control_unit.address = None
            self.run_fetch(opcode << 8 | 18, opcode, 16, r2=False)
            assert self.control_unit.register1 == 'R1'
            assert self.control_unit.register2 == 'R2'
            if not self.control_unit.address is None:
                raise AssertionError

        for opcode in {OP_HALT}:
            self.control_unit.register1 = None
            self.control_unit.register2 = None
            self.control_unit.address = None
            self.run_fetch(opcode << 8 | 18, opcode, 16, r2=False)
            assert self.control_unit.register1 is None
            assert self.control_unit.register2 is None
            if not self.control_unit.address is None:
                raise AssertionError

    def test_load(self):
        """R1 := [A1], R2 := [A2]."""
        register1, val1 = ('R3', 123456)
        register2, val2 = ('R4', 654321)
        address, val3 = (10, 111111)

        def get_register(name, size):
            """Get PC."""
            assert size == WORD_SIZE
            if name == register1:
                return val1
            if name == register2:
                return val2
            raise KeyError()

        self.registers.fetch.side_effect = get_register
        self.control_unit.address = address
        self.control_unit.register1 = register1
        self.control_unit.register2 = register2
        self.ram.put(address, val3, WORD_SIZE)
        for opcode in ARITHMETIC_OPCODES | {OP_LOAD, OP_COMP}:
            self.registers.fetch.reset_mock()
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.fetch.assert_called_once_with(register1, WORD_SIZE)
            self.registers.put.assert_has_calls([call('S', val1, WORD_SIZE),
             call('RZ', val3, WORD_SIZE)])

        for opcode in {OP_STORE}:
            self.registers.fetch.reset_mock()
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.fetch.assert_called_once_with(register1, WORD_SIZE)
            self.registers.put.assert_called_once_with('S', val1, WORD_SIZE)

        for opcode in REGISTER_OPCODES:
            self.registers.fetch.reset_mock()
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.fetch.assert_has_calls([call(register1, WORD_SIZE),
             call(register2, WORD_SIZE)])
            self.registers.put.assert_has_calls([call('S', val1, WORD_SIZE),
             call('RZ', val2, WORD_SIZE)])

        for opcode in {OP_ADDR}:
            self.registers.fetch.reset_mock()
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            assert not self.registers.fetch.called
            self.registers.put.assert_called_once_with('S', address, WORD_SIZE)

        for opcode in CONDJUMP_OPCODES | {OP_JUMP}:
            self.registers.fetch.reset_mock()
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            assert not self.registers.fetch.called
            self.registers.put.assert_called_once_with('ADDR', address, 2 * BYTE_SIZE)

        for opcode in {OP_HALT}:
            self.registers.fetch.reset_mock()
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            assert not self.registers.fetch.called
            if not not self.registers.put.called:
                raise AssertionError

    def test_basic_execute(self, should_move=None):
        """Test basic operations."""
        super().test_basic_execute(should_move=should_move)
        self.control_unit.opcode = OP_MOVE
        self.alu.move.reset_mock()
        self.control_unit.execute()
        self.alu.move.assert_called_once_with('R2', 'S')
        self.control_unit.opcode = OP_ADDR
        self.alu.move.reset_mock()
        self.control_unit.execute()
        assert not self.alu.move.called

    def run_write_back(self, should, opcode):
        """Run write back method for specific opcode."""
        print(hex(opcode), should)
        register1, next_register1, register2 = ('R5', 'R6', 'R8')
        res_register1, val1 = ('S', 123456)
        res_register2, val2 = ('RZ', 654321)
        address, canary = (10, 0)

        def get_register(name, size):
            """Get PC."""
            assert size == self.operand_size
            if name == res_register1:
                return val1
            if name == res_register2:
                return val2
            raise KeyError()

        self.registers.fetch.side_effect = get_register
        self.control_unit.address = address
        self.control_unit.register1 = register1
        self.control_unit.register2 = register2
        self.ram.put(address, canary, self.operand_size)
        self.registers.fetch.reset_mock()
        self.registers.put.reset_mock()
        self.control_unit.opcode = opcode
        self.control_unit.write_back()
        if should == 'two_registers':
            self.registers.fetch.assert_has_calls([call(res_register1, self.operand_size),
             call(res_register2, self.operand_size)])
            self.registers.put.assert_has_calls([call(register1, val1, self.operand_size),
             call(next_register1, val2, self.operand_size)])
            if not self.ram.fetch(address, self.operand_size) == canary:
                raise AssertionError
        else:
            if should == 'register':
                self.registers.fetch.assert_called_once_with(res_register1, self.operand_size)
                self.registers.put.assert_called_once_with(register1, val1, self.operand_size)
                if not self.ram.fetch(address, self.operand_size) == canary:
                    raise AssertionError
            else:
                if should == 'memory':
                    self.registers.fetch.assert_called_once_with(res_register1, self.operand_size)
                    assert not self.registers.put.called
                    if not self.ram.fetch(address, self.operand_size) == val1:
                        raise AssertionError
                else:
                    assert not self.registers.fetch.called
                    if not not self.registers.put.called:
                        raise AssertionError
        assert self.ram.fetch(address, self.operand_size) == canary

    def test_write_back(self):
        """Test write back result to the memory."""
        for opcode in {OP_SDIVMOD, OP_UDIVMOD}:
            self.run_write_back('two_registers', opcode)

        for opcode in (ARITHMETIC_OPCODES | {OP_ADDR, OP_LOAD}) - {
         OP_SDIVMOD, OP_UDIVMOD}:
            self.run_write_back('register', opcode)

        for opcode in {OP_STORE}:
            self.run_write_back('memory', opcode)

        for opcode in CONDJUMP_OPCODES | {
         OP_HALT, OP_JUMP, OP_COMP}:
            self.run_write_back('nothing', opcode)

    def test_step(self):
        """Test step cycle."""
        self.control_unit.registers = self.registers = RegisterMemory()
        for register in {'RI', 'RZ', 'S', 'R0', 'R1', 'R2', 'R3', 'R4',
         'R5', 'R6', 'R7', 'R8', 'R9', 'RA', 'RB', 'RC',
         'RD', 'RE', 'RF'}:
            self.registers.add_register(register, self.operand_size)

        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, self.operand_size, self.address_size)
        self.control_unit.alu = self.alu
        canary = 0
        self.ram.put(0, 256, WORD_SIZE)
        self.ram.put(2, 50331660, WORD_SIZE)
        self.ram.put(4, 67108878, WORD_SIZE)
        self.ram.put(6, 34603266, WORD_SIZE)
        self.ram.put(8, 8977, 2 * BYTE_SIZE)
        self.ram.put(9, 269484292, WORD_SIZE)
        self.ram.put(11, 39168, 2 * BYTE_SIZE)
        self.ram.put(12, 4294967275, WORD_SIZE)
        self.ram.put(14, 50, WORD_SIZE)
        self.ram.put(256, -123 % 2 ** WORD_SIZE, WORD_SIZE)
        self.ram.put(258, 456, WORD_SIZE)
        self.ram.put(260, canary, WORD_SIZE)
        self.registers.put('PC', 0, 2 * BYTE_SIZE)
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == -123 % 2 ** WORD_SIZE
        assert self.registers.fetch('R1', WORD_SIZE) == 0
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 2
        assert self.ram.fetch(260, WORD_SIZE) == canary
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == 2583
        assert self.registers.fetch('R1', WORD_SIZE) == 0
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 4
        assert self.ram.fetch(260, WORD_SIZE) == canary
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == 51
        x = 33
        assert self.registers.fetch('R1', WORD_SIZE) == x
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 6
        assert self.ram.fetch(260, WORD_SIZE) == canary
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == 51
        assert self.registers.fetch('R1', WORD_SIZE) == (x - 456) % 2 ** WORD_SIZE
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 8
        assert self.ram.fetch(260, WORD_SIZE) == canary
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == 51
        assert self.registers.fetch('R1', WORD_SIZE) == (x - 456) ** 2
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 9
        assert self.ram.fetch(260, WORD_SIZE) == canary
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == 51
        assert self.registers.fetch('R1', WORD_SIZE) == (x - 456) ** 2
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 11
        assert self.ram.fetch(260, WORD_SIZE) == (x - 456) ** 2
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('R0', WORD_SIZE) == 51
        assert self.registers.fetch('R1', WORD_SIZE) == (x - 456) ** 2
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 12
        assert self.control_unit.get_status() == HALTED

    def test_run(self):
        """Very simple program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        for register in {'RI', 'RZ', 'S', 'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'RA', 'RB', 'RC', 'RD', 'RE', 'RF'}:
            self.registers.add_register(register, self.operand_size)

        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, self.operand_size, self.address_size)
        self.control_unit.alu = self.alu
        self.ram.put(0, 256, WORD_SIZE)
        self.ram.put(2, 50331660, WORD_SIZE)
        self.ram.put(4, 67108878, WORD_SIZE)
        self.ram.put(6, 34603266, WORD_SIZE)
        self.ram.put(8, 8977, 2 * BYTE_SIZE)
        self.ram.put(9, 269484292, WORD_SIZE)
        self.ram.put(11, 39168, 2 * BYTE_SIZE)
        self.ram.put(12, 4294967275, WORD_SIZE)
        self.ram.put(14, 50, WORD_SIZE)
        self.ram.put(256, 4294967173, WORD_SIZE)
        self.ram.put(258, 456, WORD_SIZE)
        self.registers.put('PC', 0, 2 * BYTE_SIZE)
        self.control_unit.run()
        assert self.ram.fetch(260, WORD_SIZE) == 178929
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 12
        assert self.control_unit.get_status() == HALTED

    def test_minimal_run(self):
        """Minimal program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', self.operand_size)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, self.operand_size, self.address_size)
        self.control_unit.alu = self.alu
        self.ram.put(0, 39168, 2 * BYTE_SIZE)
        self.registers.put('PC', 0, 2 * BYTE_SIZE)
        self.control_unit.run()
        assert self.registers.fetch('PC', 2 * BYTE_SIZE) == 1
        assert self.control_unit.get_status() == HALTED