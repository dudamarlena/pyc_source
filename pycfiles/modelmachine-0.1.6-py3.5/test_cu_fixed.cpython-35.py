# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/tests/test_cu_fixed.py
# Compiled at: 2016-02-09 07:36:55
# Size of source mod 2**32: 27634 bytes
"""Test case for control unit with fixed command length."""
from unittest.mock import call
from pytest import raises
from modelmachine.cu import RUNNING, HALTED
from modelmachine.cu import ControlUnit3
from modelmachine.cu import ControlUnit2
from modelmachine.cu import ControlUnit1
from modelmachine.memory import RegisterMemory, RandomAccessMemory
from modelmachine.alu import ArithmeticLogicUnit, LESS, GREATER, EQUAL
from .test_cu_abstract import BYTE_SIZE, WORD_SIZE, OP_MOVE, OP_SDIVMOD, OP_COMP, OP_UDIVMOD, OP_JUMP, OP_JEQ, OP_LOAD, OP_STORE, OP_SWAP, OP_JNEQ, OP_SJL, OP_SJGEQ, OP_SJLEQ, OP_SJG, OP_UJL, OP_UJGEQ, OP_UJLEQ, OP_UJG, OP_HALT, ARITHMETIC_OPCODES, CONDJUMP_OPCODES
from .test_cu_abstract import TestControlUnit as TBCU

class TestControlUnit3(TBCU):
    __doc__ = 'Test case for  Mode Machine 3 Control Unit.'

    def setup(self):
        """Init state."""
        super().setup()
        self.ram = RandomAccessMemory(WORD_SIZE, 256, 'big')
        self.control_unit = ControlUnit3(WORD_SIZE, BYTE_SIZE, self.registers, self.ram, self.alu, WORD_SIZE)
        assert self.control_unit.opcodes == {0, 1, 2, 3, 4,
         19, 20,
         128, 129, 130,
         131, 132, 133, 134,
         147, 148, 149, 150,
         153}

    def test_fetch_and_decode(self):
        """Right fetch and decode is a half of business."""
        for opcode in self.control_unit.opcodes:
            self.control_unit.address1, self.control_unit.address2 = (None, None)
            self.run_fetch(opcode << 24 | 131844, opcode, WORD_SIZE)
            assert self.control_unit.address1 == 2
            assert self.control_unit.address2 == 3
            if not self.control_unit.address3 == 4:
                raise AssertionError

        for opcode in set(range(2 ** BYTE_SIZE)) - self.control_unit.opcodes:
            with raises(ValueError):
                self.run_fetch(opcode << 24 | 131844, opcode, WORD_SIZE)

    def test_load(self):
        """R1 := [A1], R2 := [A2]."""
        addr1, val1 = (5, 123456)
        addr2, val2 = (10, 654321)
        addr3 = 15
        self.ram.put(addr1, val1, WORD_SIZE)
        self.ram.put(addr2, val2, WORD_SIZE)
        self.control_unit.address1 = addr1
        self.control_unit.address2 = addr2
        self.control_unit.address3 = addr3
        for opcode in ARITHMETIC_OPCODES:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_has_calls([call('R1', val1, WORD_SIZE),
             call('R2', val2, WORD_SIZE)])

        for opcode in CONDJUMP_OPCODES:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_has_calls([call('R1', val1, WORD_SIZE),
             call('R2', val2, WORD_SIZE),
             call('ADDR', addr3, BYTE_SIZE)])

        for opcode in {OP_MOVE}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('R1', val1, WORD_SIZE)

        for opcode in {OP_JUMP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('ADDR', addr3, BYTE_SIZE)

        for opcode in {OP_HALT}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            if not not self.registers.put.called:
                raise AssertionError

    def test_basic_execute(self, should_move=True):
        """Test basic operations."""
        super().test_basic_execute(should_move)
        for opcode in range(0, 256):
            if opcode not in self.control_unit.opcodes:
                with raises(ValueError):
                    self.control_unit.opcode = opcode
                    self.control_unit.execute()

    def run_cond_jump(self, opcode, signed, mol, equal):
        """Run one conditional jump test."""
        self.alu.cond_jump.reset_mock()
        self.alu.sub.reset_mock()
        self.registers.put.reset_mock()
        self.control_unit.opcode = opcode
        self.control_unit.execute()
        self.alu.sub.assert_called_once_with()
        assert not self.registers.put.called
        self.alu.cond_jump.assert_called_once_with(signed, mol, equal)

    def test_execute_cond_jumps(self):
        """Test for jumps."""
        self.run_cond_jump(OP_JEQ, True, EQUAL, True)
        self.run_cond_jump(OP_JNEQ, True, EQUAL, False)
        self.run_cond_jump(OP_SJL, True, LESS, False)
        self.run_cond_jump(OP_SJGEQ, True, GREATER, True)
        self.run_cond_jump(OP_SJLEQ, True, LESS, True)
        self.run_cond_jump(OP_SJG, True, GREATER, False)
        self.run_cond_jump(OP_UJL, False, LESS, False)
        self.run_cond_jump(OP_UJGEQ, False, GREATER, True)
        self.run_cond_jump(OP_UJLEQ, False, LESS, True)
        self.run_cond_jump(OP_UJG, False, GREATER, False)

    def test_execute_jump_halt(self):
        """Test for jump and halt."""
        self.alu.cond_jump.reset_mock()
        self.alu.sub.reset_mock()
        self.registers.put.reset_mock()
        self.control_unit.opcode = OP_JUMP
        self.control_unit.execute()
        assert not self.alu.sub.called
        assert not self.registers.put.called
        self.alu.jump.assert_called_once_with()
        self.control_unit.opcode = OP_HALT
        self.control_unit.execute()
        assert not self.alu.sub.called
        assert not self.registers.put.called
        self.alu.halt.assert_called_once_with()

    def run_write_back(self, should, opcode):
        """Run write back method for specific opcode."""
        first, second, third = (11111111, 22222222, 33333333)
        size = WORD_SIZE // self.ram.word_size

        def get_register(name, size):
            """Get result."""
            assert name in {'R1', 'S'}
            assert size == WORD_SIZE
            if name == 'S':
                return second
            if name == 'R1':
                return third

        self.registers.fetch.side_effect = get_register
        for address in (10, 2 ** BYTE_SIZE - size):
            next_address = (address + size) % 2 ** BYTE_SIZE
            self.ram.put(address, first, WORD_SIZE)
            self.ram.put(next_address, first, WORD_SIZE)
            self.control_unit.address3 = address
            self.control_unit.opcode = opcode
            self.control_unit.write_back()
            if should:
                assert self.ram.fetch(address, WORD_SIZE) == second
                if opcode in {OP_SDIVMOD,
                 OP_UDIVMOD}:
                    if not self.ram.fetch(next_address, WORD_SIZE) == third:
                        raise AssertionError
                elif not self.ram.fetch(next_address, WORD_SIZE) == first:
                    raise AssertionError
            elif not self.ram.fetch(address, WORD_SIZE) == first:
                raise AssertionError

    def test_write_back(self):
        """Test write back result to the memory."""
        for opcode in ARITHMETIC_OPCODES | {OP_MOVE}:
            self.run_write_back(True, opcode)

        for opcode in CONDJUMP_OPCODES | {
         OP_HALT,
         OP_JUMP}:
            self.run_write_back(False, opcode)

    def test_step(self):
        """Test step cycle."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 16909060, WORD_SIZE)
        self.ram.put(1, 2181169925, WORD_SIZE)
        self.ram.put(2, 12, WORD_SIZE)
        self.ram.put(3, 10, WORD_SIZE)
        self.ram.put(5, 2566914048, WORD_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 1
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('PC', BYTE_SIZE) == 5
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('PC', BYTE_SIZE) == 6
        assert self.control_unit.get_status() == HALTED

    def test_run(self):
        """Very simple program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 16909060, WORD_SIZE)
        self.ram.put(1, 2181169925, WORD_SIZE)
        self.ram.put(2, 12, WORD_SIZE)
        self.ram.put(3, 10, WORD_SIZE)
        self.ram.put(5, 2566914048, WORD_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.run()
        assert self.ram.fetch(4, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 6
        assert self.control_unit.get_status() == HALTED


class TestControlUnit2(TestControlUnit3):
    __doc__ = 'Test case for  Mode Machine 3 Control Unit.'

    def setup(self):
        """Init state."""
        super().setup()
        self.control_unit = ControlUnit2(WORD_SIZE, BYTE_SIZE, self.registers, self.ram, self.alu, WORD_SIZE)
        assert self.control_unit.opcodes == {0, 1, 2, 3, 4,
         19, 20,
         5,
         128, 129, 130,
         131, 132, 133, 134,
         147, 148, 149, 150,
         153}

    def test_fetch_and_decode(self):
        """Right fetch and decode is a half of business."""
        for opcode in self.control_unit.opcodes:
            self.control_unit.address1, self.control_unit.address2 = (None, None)
            self.run_fetch(opcode << 24 | 515, opcode, WORD_SIZE)
            assert self.control_unit.address1 == 2
            if not self.control_unit.address2 == 3:
                raise AssertionError

        for opcode in set(range(2 ** BYTE_SIZE)) - self.control_unit.opcodes:
            with raises(ValueError):
                self.run_fetch(opcode << 24 | 515, opcode, WORD_SIZE)

    def test_load(self):
        """R1 := [A1], R2 := [A2]."""
        addr1, val1 = (5, 123456)
        addr2, val2 = (10, 654321)
        self.ram.put(addr1, val1, WORD_SIZE)
        self.ram.put(addr2, val2, WORD_SIZE)
        self.control_unit.address1 = addr1
        self.control_unit.address2 = addr2
        for opcode in ARITHMETIC_OPCODES | {
         OP_COMP}:
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

        for opcode in CONDJUMP_OPCODES | {
         OP_JUMP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('ADDR', addr2, BYTE_SIZE)

        for opcode in {OP_HALT}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            if not not self.registers.put.called:
                raise AssertionError

    def run_cond_jump(self, opcode, signed, mol, equal):
        """Run one conditional jump test."""
        self.alu.cond_jump.reset_mock()
        self.alu.sub.reset_mock()
        self.registers.put.reset_mock()
        self.control_unit.opcode = opcode
        self.control_unit.execute()
        assert not self.alu.sub.called
        assert not self.registers.put.called
        self.alu.cond_jump.assert_called_once_with(signed, mol, equal)

    def test_execute_comp(self):
        """Test for comp."""
        self.alu.cond_jump.reset_mock()
        self.alu.sub.reset_mock()
        self.registers.put.reset_mock()
        self.control_unit.opcode = OP_COMP
        self.control_unit.execute()
        assert not self.registers.put.called
        self.alu.sub.assert_called_once_with()

    def run_write_back(self, should, opcode):
        """Run write back method for specific opcode."""
        first, second, third = (11111111, 22222222, 33333333)
        size = WORD_SIZE // self.ram.word_size

        def get_register(name, size):
            """Get result."""
            assert name in {'R1', 'R2'}
            assert size == WORD_SIZE
            if name == 'R1':
                return second
            if name == 'R2':
                return third

        self.registers.fetch.side_effect = get_register
        for address in (10, 2 ** BYTE_SIZE - size):
            next_address = (address + size) % 2 ** BYTE_SIZE
            self.ram.put(address, first, WORD_SIZE)
            self.ram.put(next_address, first, WORD_SIZE)
            self.control_unit.address1 = address
            self.control_unit.opcode = opcode
            self.control_unit.write_back()
            if should:
                assert self.ram.fetch(address, WORD_SIZE) == second
                if opcode in {OP_SDIVMOD, OP_UDIVMOD}:
                    if not self.ram.fetch(next_address, WORD_SIZE) == third:
                        raise AssertionError
                elif not self.ram.fetch(next_address, WORD_SIZE) == first:
                    raise AssertionError
            elif not self.ram.fetch(address, WORD_SIZE) == first:
                raise AssertionError

    def test_write_back(self):
        """Test write back result to the memory."""
        for opcode in ARITHMETIC_OPCODES | {OP_MOVE}:
            self.run_write_back(True, opcode)

        for opcode in CONDJUMP_OPCODES | {
         OP_HALT,
         OP_JUMP,
         OP_COMP}:
            self.run_write_back(False, opcode)

    def test_step(self):
        """Test step cycle."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 16777988, WORD_SIZE)
        self.ram.put(1, 83886853, WORD_SIZE)
        self.ram.put(2, 2248146950, WORD_SIZE)
        self.ram.put(3, 12, WORD_SIZE)
        self.ram.put(4, 10, WORD_SIZE)
        self.ram.put(5, 20, WORD_SIZE)
        self.ram.put(6, 2566914048, WORD_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.step()
        assert self.ram.fetch(3, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 1
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(3, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 2
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('PC', BYTE_SIZE) == 6
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.registers.fetch('PC', BYTE_SIZE) == 7
        assert self.control_unit.get_status() == HALTED

    def test_run(self):
        """Very simple program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 16777988, WORD_SIZE)
        self.ram.put(1, 83886853, WORD_SIZE)
        self.ram.put(2, 2248146950, WORD_SIZE)
        self.ram.put(3, 12, WORD_SIZE)
        self.ram.put(4, 10, WORD_SIZE)
        self.ram.put(5, 20, WORD_SIZE)
        self.ram.put(6, 2566914048, WORD_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.run()
        assert self.ram.fetch(3, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 7
        assert self.control_unit.get_status() == HALTED


class TestControlUnit1(TestControlUnit2):
    __doc__ = 'Test case for  Mode Machine 1 Control Unit.'

    def setup(self):
        """Init state."""
        super().setup()
        self.control_unit = ControlUnit1(WORD_SIZE, BYTE_SIZE, self.registers, self.ram, self.alu, WORD_SIZE)
        assert self.control_unit.opcodes == {0, 16, 32,
         1, 2, 3, 4,
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
                self.run_fetch(opcode << 24, opcode, WORD_SIZE)

        for opcode in self.control_unit.opcodes:
            self.control_unit.address = None
            self.run_fetch(opcode << 24 | 2, opcode, WORD_SIZE)
            if not self.control_unit.address == 2:
                raise AssertionError

    def test_load(self):
        """R1 := [A1], R2 := [A2]."""
        addr, val = (5, 123456)
        self.ram.put(addr, val, WORD_SIZE)
        self.control_unit.address = addr
        for opcode in ARITHMETIC_OPCODES | {OP_COMP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('R', val, WORD_SIZE)

        for opcode in {OP_LOAD}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('S', val, WORD_SIZE)

        for opcode in CONDJUMP_OPCODES | {OP_JUMP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            self.registers.put.assert_called_once_with('ADDR', addr, BYTE_SIZE)

        for opcode in {OP_HALT, OP_STORE, OP_SWAP}:
            self.registers.put.reset_mock()
            self.control_unit.opcode = opcode
            self.control_unit.load()
            if not not self.registers.put.called:
                raise AssertionError

    def test_basic_execute(self, should_move=False):
        """Test basic operations."""
        super().test_basic_execute(should_move)

    def test_execute_comp(self):
        """Test for comp."""
        value = 123
        self.alu.cond_jump.reset_mock()
        self.alu.sub.reset_mock()
        self.registers.put.reset_mock()
        self.registers.fetch.reset_mock()
        self.registers.fetch.return_value = value
        self.control_unit.opcode = OP_COMP
        self.control_unit.execute()
        self.registers.fetch.assert_called_once_with('S', WORD_SIZE)
        self.alu.sub.assert_called_once_with()
        self.registers.put.assert_called_once_with('S', value, WORD_SIZE)

    def test_execute_load_store_swap(self):
        """Test for load, store and swap."""
        self.alu.cond_jump.reset_mock()
        self.alu.sub.reset_mock()
        self.registers.put.reset_mock()
        self.control_unit.opcode = OP_LOAD
        self.control_unit.execute()
        assert not self.alu.sub.called
        assert not self.alu.move.called
        assert not self.alu.jump.called
        assert not self.alu.swap.called
        assert not self.alu.cond_jump.called
        assert not self.registers.put.called
        self.control_unit.opcode = OP_STORE
        self.control_unit.execute()
        assert not self.alu.sub.called
        assert not self.alu.move.called
        assert not self.alu.jump.called
        assert not self.alu.swap.called
        assert not self.alu.cond_jump.called
        assert not self.registers.put.called
        self.control_unit.opcode = OP_SWAP
        self.control_unit.execute()
        assert not self.alu.sub.called
        assert not self.alu.move.called
        assert not self.alu.jump.called
        assert not self.alu.cond_jump.called
        assert not self.registers.put.called
        self.alu.swap.assert_called_once_with()

    def run_write_back(self, should, opcode):
        """Run write back method for specific opcode."""
        first, second = (11111111, 22222222)
        size = WORD_SIZE // self.ram.word_size
        self.registers.fetch.return_value = second
        for address in (10, 2 ** BYTE_SIZE - size):
            self.registers.fetch.reset_mock()
            next_address = (address + size) % 2 ** BYTE_SIZE
            self.ram.put(address, first, WORD_SIZE)
            self.ram.put(next_address, first, WORD_SIZE)
            self.control_unit.address = address
            self.control_unit.opcode = opcode
            self.control_unit.write_back()
            if should:
                self.registers.fetch.assert_called_once_with('S', WORD_SIZE)
                assert self.ram.fetch(address, WORD_SIZE) == second
                if not self.ram.fetch(next_address, WORD_SIZE) == first:
                    raise AssertionError
            else:
                assert not self.registers.fetch.called
                if not self.ram.fetch(address, WORD_SIZE) == first:
                    raise AssertionError

    def test_write_back(self):
        """Test write back result to the memory."""
        for opcode in ARITHMETIC_OPCODES | CONDJUMP_OPCODES | {
         OP_LOAD, OP_SWAP, OP_JUMP, OP_HALT}:
            self.run_write_back(False, opcode)

        for opcode in {OP_STORE}:
            self.run_write_back(True, opcode)

    def test_step(self):
        """Test step cycle."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 4, WORD_SIZE)
        self.ram.put(1, 16777221, WORD_SIZE)
        self.ram.put(2, 83886086, WORD_SIZE)
        self.ram.put(3, 2248146951, WORD_SIZE)
        self.ram.put(4, 12, WORD_SIZE)
        self.ram.put(5, 10, WORD_SIZE)
        self.ram.put(6, 20, WORD_SIZE)
        self.ram.put(7, 268435460, WORD_SIZE)
        self.ram.put(8, 2566914048, WORD_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 12
        assert self.registers.fetch('PC', BYTE_SIZE) == 1
        assert self.registers.fetch('S', WORD_SIZE) == 12
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 12
        assert self.registers.fetch('PC', BYTE_SIZE) == 2
        assert self.registers.fetch('S', WORD_SIZE) == 22
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 12
        assert self.registers.fetch('PC', BYTE_SIZE) == 3
        assert self.registers.fetch('S', WORD_SIZE) == 22
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 12
        assert self.registers.fetch('PC', BYTE_SIZE) == 7
        assert self.registers.fetch('S', WORD_SIZE) == 22
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 8
        assert self.registers.fetch('S', WORD_SIZE) == 22
        assert self.control_unit.get_status() == RUNNING
        self.control_unit.step()
        assert self.ram.fetch(4, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 9
        assert self.registers.fetch('S', WORD_SIZE) == 22
        assert self.control_unit.get_status() == HALTED

    def test_run(self):
        """Very simple program."""
        self.control_unit.registers = self.registers = RegisterMemory()
        self.registers.add_register('RI', WORD_SIZE)
        self.alu = ArithmeticLogicUnit(self.registers, self.control_unit.register_names, WORD_SIZE, BYTE_SIZE)
        self.control_unit.alu = self.alu
        self.ram.put(0, 4, WORD_SIZE)
        self.ram.put(1, 16777221, WORD_SIZE)
        self.ram.put(2, 83886086, WORD_SIZE)
        self.ram.put(3, 2248146951, WORD_SIZE)
        self.ram.put(4, 12, WORD_SIZE)
        self.ram.put(5, 10, WORD_SIZE)
        self.ram.put(6, 20, WORD_SIZE)
        self.ram.put(7, 268435460, WORD_SIZE)
        self.ram.put(8, 2566914048, WORD_SIZE)
        self.registers.put('PC', 0, BYTE_SIZE)
        self.control_unit.run()
        assert self.ram.fetch(4, WORD_SIZE) == 22
        assert self.registers.fetch('PC', BYTE_SIZE) == 9
        assert self.registers.fetch('S', WORD_SIZE) == 22
        assert self.control_unit.get_status() == HALTED