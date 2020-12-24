# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/cu.py
# Compiled at: 2016-03-05 12:27:04
# Size of source mod 2**32: 27494 bytes
"""Control unit parse instruction and give the commands to another part of computer."""
from modelmachine.alu import HALT, LESS, GREATER, EQUAL
from modelmachine.numeric import Integer
RUNNING = 1
HALTED = 2

class AbstractControlUnit:
    __doc__ = 'Abstract control unit allow to execute two methods: step and run.'

    def __init__(self, registers, ram, alu, operand_size):
        """See help(type(x))."""
        self.registers = registers
        self.ram = ram
        self.alu = alu
        self.operand_size = operand_size

    def step(self):
        """Execution of one instruction."""
        self.fetch_and_decode()
        self.load()
        self.execute()
        self.write_back()

    def get_status(self):
        """Show, can we or not execute another one instruction."""
        if self.registers.fetch('FLAGS', self.operand_size) & HALT != 0:
            return HALTED
        else:
            return RUNNING

    def run(self):
        """Execute instruction one-by-one until we met HALT command."""
        while self.get_status() == RUNNING:
            self.step()

    def fetch_and_decode(self):
        """Fetch instruction and decode them. At last, method should increment PC.

        Recommendation: set up address registers A1, A2, AS for loading
        into operation registers R1, R2, S.
        """
        raise NotImplementedError()

    def load(self):
        """Load data from memory to operation registers."""
        raise NotImplementedError()

    def execute(self):
        """Send message to ALU."""
        raise NotImplementedError()

    def write_back(self):
        """Save result of calculation to memory."""
        raise NotImplementedError()


class ControlUnit(AbstractControlUnit):
    __doc__ = 'Abstract control unit (need to inherit to determine machine).'
    START_ADDRESS = 0
    OPCODES = {'move': 0, 
     'load': 0, 
     'add': 1, 
     'sub': 2, 
     'smul': 3, 
     'sdivmod': 4, 
     'comp': 5, 
     'store': 16, 
     'addr': 17, 
     'umul': 19, 
     'udivmod': 20, 
     'swap': 32, 
     'rmove': 32, 
     'radd': 33, 
     'rsub': 34, 
     'rsmul': 35, 
     'rsdivmod': 36, 
     'rcomp': 37, 
     'rumul': 51, 
     'rudivmod': 52, 
     'stpush': 90, 
     'stpop': 91, 
     'stdup': 92, 
     'stswap': 93, 
     'jump': 128, 
     'jeq': 129, 
     'jneq': 130, 
     'sjl': 131, 
     'sjgeq': 132, 
     'sjleq': 133, 
     'sjg': 134, 
     'ujl': 147, 
     'ujgeq': 148, 
     'ujleq': 149, 
     'ujg': 150, 
     'halt': 153}
    OPCODE_SIZE = 8
    ARITHMETIC_OPCODES = {OPCODES['add'], OPCODES['sub'],
     OPCODES['smul'], OPCODES['sdivmod'],
     OPCODES['umul'], OPCODES['udivmod']}
    DIVMOD_OPCODES = {OPCODES['sdivmod'], OPCODES['udivmod']}
    CONDJUMP_OPCODES = {
     OPCODES['jeq'], OPCODES['jneq'],
     OPCODES['sjl'], OPCODES['sjgeq'],
     OPCODES['sjleq'], OPCODES['sjg'],
     OPCODES['ujl'], OPCODES['ujgeq'],
     OPCODES['ujleq'], OPCODES['ujg']}
    JUMP_OPCODES = CONDJUMP_OPCODES | {OPCODES['jump']}
    STACK_OPCODES = {OPCODES['stpush'], OPCODES['stpop'],
     OPCODES['stdup'], OPCODES['stswap']}
    BINAR_OPCODES = ARITHMETIC_OPCODES | {OPCODES['comp']}
    register_names = {'PC': 'PC', 'ADDR': 'ADDR', 'RI': 'RI'}
    opcode = 0
    opcodes = None

    def __init__(self, ir_size, address_size, *vargs, **kvargs):
        """Create necessary registers."""
        super().__init__(*vargs, **kvargs)
        self.ir_size = ir_size
        self.address_size = address_size
        for reg in {'PC', 'ADDR'}:
            self.registers.add_register(reg, self.address_size)

        self.registers.add_register('RI', self.ir_size)
        self.registers.put('PC', self.START_ADDRESS, self.address_size)

    def fetch_instruction(self, instruction_size):
        """Read instruction and fetch opcode."""
        instruction_pointer = self.registers.fetch(self.register_names['PC'], self.address_size)
        instruction = self.ram.fetch(instruction_pointer, instruction_size)
        self.registers.put(self.register_names['RI'], instruction, self.ir_size)
        self.opcode = instruction >> instruction_size - self.OPCODE_SIZE
        if self.opcodes and self.opcode not in self.opcodes:
            raise ValueError('Invalid opcode `{opcode}`'.format(opcode=hex(self.opcode)))
        instruction_pointer += instruction_size // self.ram.word_size
        self.registers.put(self.register_names['PC'], instruction_pointer, self.address_size)
        return instruction

    def execute(self):
        """Run arithmetic instructions."""
        if self.opcode == self.OPCODES['move']:
            self.alu.move()
        else:
            if self.opcode == self.OPCODES['halt']:
                self.alu.halt()
            else:
                if self.opcode == self.OPCODES['add']:
                    self.alu.add()
                else:
                    if self.opcode == self.OPCODES['sub']:
                        self.alu.sub()
                    else:
                        if self.opcode == self.OPCODES['smul']:
                            self.alu.smul()
                        else:
                            if self.opcode == self.OPCODES['umul']:
                                self.alu.umul()
                            else:
                                if self.opcode == self.OPCODES['sdivmod']:
                                    self.alu.sdivmod()
                                else:
                                    if self.opcode == self.OPCODES['udivmod']:
                                        self.alu.udivmod()
                                    else:
                                        raise ValueError('Invalid opcode `{opcode}`'.format(opcode=hex(self.opcode)))

    def execute_jump(self):
        """Conditional jump part of execution."""
        if self.opcode == self.OPCODES['jump']:
            self.alu.jump()
        else:
            if self.opcode == self.OPCODES['jeq']:
                self.alu.cond_jump(True, EQUAL, True)
            else:
                if self.opcode == self.OPCODES['jneq']:
                    self.alu.cond_jump(True, EQUAL, False)
                else:
                    if self.opcode == self.OPCODES['sjl']:
                        self.alu.cond_jump(True, LESS, False)
                    else:
                        if self.opcode == self.OPCODES['sjgeq']:
                            self.alu.cond_jump(True, GREATER, True)
                        else:
                            if self.opcode == self.OPCODES['sjleq']:
                                self.alu.cond_jump(True, LESS, True)
                            else:
                                if self.opcode == self.OPCODES['sjg']:
                                    self.alu.cond_jump(True, GREATER, False)
                                else:
                                    if self.opcode == self.OPCODES['ujl']:
                                        self.alu.cond_jump(False, LESS, False)
                                    else:
                                        if self.opcode == self.OPCODES['ujgeq']:
                                            self.alu.cond_jump(False, GREATER, True)
                                        else:
                                            if self.opcode == self.OPCODES['ujleq']:
                                                self.alu.cond_jump(False, LESS, True)
                                            elif self.opcode == self.OPCODES['ujg']:
                                                self.alu.cond_jump(False, GREATER, False)

    def fetch_and_decode(self):
        """Fetch instruction and addresses."""
        raise NotImplementedError()

    def load(self):
        """Load data to registers R1 and R2."""
        raise NotImplementedError()

    def write_back(self):
        """Write back calculation result."""
        raise NotImplementedError()


class ControlUnit3(ControlUnit):
    __doc__ = 'Control unit for model-machine-3.'
    address1 = 0
    address2 = 0
    address3 = 0
    register_names = {'PC': 'PC', 'ADDR': 'ADDR', 'RI': 'RI', 
     'R1': 'R1', 'R2': 'R2', 'S': 'S', 'RES': 'R1', 
     'FLAGS': 'FLAGS'}

    def __init__(self, ir_size, *vargs, **kvargs):
        """See help(type(x))."""
        super().__init__(ir_size, *vargs, **kvargs)
        self.instruction_size = ir_size
        self.opcodes = self.ARITHMETIC_OPCODES | self.JUMP_OPCODES | {
         self.OPCODES['move'],
         self.OPCODES['halt']}
        for reg in {'R1', 'R2', 'FLAGS'}:
            self.registers.add_register(reg, self.operand_size)

    def fetch_and_decode(self):
        """Fetch 3 addresses."""
        instruction = self.fetch_instruction(self.instruction_size)
        mask = 2 ** self.address_size - 1
        self.address1 = instruction >> 2 * self.address_size & mask
        self.address2 = instruction >> self.address_size & mask
        self.address3 = instruction & mask

    def load(self):
        """Load registers R1 and R2."""
        if self.opcode in self.ARITHMETIC_OPCODES or self.opcode in self.CONDJUMP_OPCODES or self.opcode == self.OPCODES['move']:
            operand1 = self.ram.fetch(self.address1, self.operand_size)
            self.registers.put(self.register_names['R1'], operand1, self.operand_size)
            if self.opcode != self.OPCODES['move']:
                operand2 = self.ram.fetch(self.address2, self.operand_size)
                self.registers.put(self.register_names['R2'], operand2, self.operand_size)
            if self.opcode in self.JUMP_OPCODES:
                self.registers.put(self.register_names['ADDR'], self.address3, self.address_size)

    def execute(self):
        """Add specific commands: conditional jumps."""
        if self.opcode in self.JUMP_OPCODES:
            if self.opcode != self.OPCODES['jump']:
                self.alu.sub()
            self.execute_jump()
        else:
            super().execute()

    def write_back(self):
        """Write result back."""
        if self.opcode in self.ARITHMETIC_OPCODES or self.opcode == self.OPCODES['move']:
            value = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.ram.put(self.address3, value, self.operand_size)
            if self.opcode in self.DIVMOD_OPCODES:
                address = self.address3 + self.operand_size // self.ram.word_size
                address %= self.ram.memory_size
                value = self.registers.fetch(self.register_names['RES'], self.operand_size)
                self.ram.put(address, value, self.operand_size)


class ControlUnit2(ControlUnit):
    __doc__ = 'Control unit for model-machine-2.'
    address1 = 0
    address2 = 0
    register_names = {'PC': 'PC', 'ADDR': 'ADDR', 'RI': 'RI', 
     'R1': 'R1', 'R2': 'R2', 'S': 'R1', 'RES': 'R2', 
     'FLAGS': 'FLAGS'}

    def __init__(self, ir_size, *vargs, **kvargs):
        """See help(type(x))."""
        super().__init__(ir_size, *vargs, **kvargs)
        self.instruction_size = ir_size
        self.opcodes = self.ARITHMETIC_OPCODES | self.JUMP_OPCODES | {
         self.OPCODES['move'],
         self.OPCODES['halt'],
         self.OPCODES['comp']}
        for reg in {'R1', 'R2', 'FLAGS'}:
            self.registers.add_register(reg, self.operand_size)

    def fetch_and_decode(self):
        """Fetch 3 addresses."""
        instruction = self.fetch_instruction(self.instruction_size)
        mask = 2 ** self.address_size - 1
        self.address1 = instruction >> self.address_size & mask
        self.address2 = instruction & mask

    def load(self):
        """Load registers R1 and R2."""
        if self.opcode in self.BINAR_OPCODES:
            operand1 = self.ram.fetch(self.address1, self.operand_size)
            self.registers.put(self.register_names['R1'], operand1, self.operand_size)
            operand2 = self.ram.fetch(self.address2, self.operand_size)
            self.registers.put(self.register_names['R2'], operand2, self.operand_size)
        else:
            if self.opcode == self.OPCODES['move']:
                operand1 = self.ram.fetch(self.address2, self.operand_size)
                self.registers.put(self.register_names['R1'], operand1, self.operand_size)
            elif self.opcode in self.JUMP_OPCODES:
                self.registers.put(self.register_names['ADDR'], self.address2, self.address_size)

    def execute(self):
        """Add specific commands: conditional jumps and cmp."""
        if self.opcode == self.OPCODES['comp']:
            self.alu.sub()
        else:
            if self.opcode in self.JUMP_OPCODES:
                self.execute_jump()
            else:
                super().execute()

    def write_back(self):
        """Write result back."""
        if self.opcode in self.ARITHMETIC_OPCODES | {self.OPCODES['move']}:
            value = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.ram.put(self.address1, value, self.operand_size)
            if self.opcode in self.DIVMOD_OPCODES:
                address = self.address1 + self.operand_size // self.ram.word_size
                address %= self.ram.memory_size
                value = self.registers.fetch(self.register_names['RES'], self.operand_size)
                self.ram.put(address, value, self.operand_size)


class ControlUnitV(ControlUnit):
    __doc__ = 'Control unit for model-machine-variable.'
    address1 = 0
    address2 = 0
    register_names = {'PC': 'PC', 'ADDR': 'ADDR', 'RI': 'RI', 
     'R1': 'R1', 'R2': 'R2', 'S': 'R1', 'RES': 'R2', 
     'FLAGS': 'FLAGS'}

    def __init__(self, ir_size, *vargs, **kvargs):
        """See help(type(x))."""
        super().__init__(ir_size, *vargs, **kvargs)
        self.opcodes = self.ARITHMETIC_OPCODES | self.JUMP_OPCODES | {
         self.OPCODES['move'],
         self.OPCODES['halt'],
         self.OPCODES['comp']}
        for reg in {'R1', 'R2', 'FLAGS'}:
            self.registers.add_register(reg, self.operand_size)

    def fetch_and_decode(self):
        """Fetch 3 addresses."""
        mask = 2 ** self.address_size - 1
        two_operands = self.BINAR_OPCODES | {self.OPCODES['move']}
        instruction_pointer = self.registers.fetch(self.register_names['PC'], self.address_size)
        self.opcode = self.ram.fetch(instruction_pointer, self.OPCODE_SIZE)
        if self.opcode in two_operands:
            instruction_size = self.OPCODE_SIZE + 2 * self.address_size
        else:
            if self.opcode in self.JUMP_OPCODES:
                instruction_size = self.OPCODE_SIZE + self.address_size
            else:
                instruction_size = self.OPCODE_SIZE
            instruction = self.fetch_instruction(instruction_size)
            if self.opcode in two_operands:
                self.address1 = instruction >> self.address_size & mask
                self.address2 = instruction & mask
            elif self.opcode in self.JUMP_OPCODES:
                self.address1 = instruction & mask

    def load(self):
        """Load registers R1 and R2."""
        if self.opcode in self.BINAR_OPCODES:
            operand1 = self.ram.fetch(self.address1, self.operand_size)
            self.registers.put(self.register_names['R1'], operand1, self.operand_size)
            operand2 = self.ram.fetch(self.address2, self.operand_size)
            self.registers.put(self.register_names['R2'], operand2, self.operand_size)
        else:
            if self.opcode == self.OPCODES['move']:
                operand1 = self.ram.fetch(self.address2, self.operand_size)
                self.registers.put(self.register_names['R1'], operand1, self.operand_size)
            elif self.opcode in self.JUMP_OPCODES:
                self.registers.put(self.register_names['ADDR'], self.address1, self.address_size)

    def execute(self):
        """Add specific commands: conditional jumps and cmp."""
        if self.opcode == self.OPCODES['comp']:
            self.alu.sub()
        else:
            if self.opcode in self.JUMP_OPCODES:
                self.execute_jump()
            else:
                super().execute()

    def write_back(self):
        """Write result back."""
        if self.opcode in self.ARITHMETIC_OPCODES | {self.OPCODES['move']}:
            value = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.ram.put(self.address1, value, self.operand_size)
            if self.opcode in self.DIVMOD_OPCODES:
                address = self.address1 + self.operand_size // self.ram.word_size
                address %= self.ram.memory_size
                value = self.registers.fetch(self.register_names['RES'], self.operand_size)
                self.ram.put(address, value, self.operand_size)


class ControlUnit1(ControlUnit):
    __doc__ = 'Control unit for model machine 1.'
    address = 0
    register_names = {'PC': 'PC', 'ADDR': 'ADDR', 'RI': 'RI', 
     'R1': 'S', 'R2': 'R', 'S': 'S', 'RES': 'S1', 
     'FLAGS': 'FLAGS'}

    def __init__(self, ir_size, *vargs, **kvargs):
        """See help(type(x))."""
        super().__init__(ir_size, *vargs, **kvargs)
        self.instruction_size = ir_size
        self.opcodes = self.ARITHMETIC_OPCODES | self.JUMP_OPCODES | {
         self.OPCODES['load'],
         self.OPCODES['store'],
         self.OPCODES['swap'],
         self.OPCODES['halt'],
         self.OPCODES['comp']}
        for reg in {'S', 'S1', 'R', 'FLAGS'}:
            self.registers.add_register(reg, self.operand_size)

    def fetch_and_decode(self):
        """Fetch 3 addresses."""
        instruction = self.fetch_instruction(self.instruction_size)
        mask = 2 ** self.address_size - 1
        self.address = instruction & mask

    def load(self):
        """Load registers R1 and R2."""
        if self.opcode in self.ARITHMETIC_OPCODES | {self.OPCODES['comp']}:
            operand = self.ram.fetch(self.address, self.operand_size)
            self.registers.put(self.register_names['R2'], operand, self.operand_size)
        else:
            if self.opcode == self.OPCODES['load']:
                operand = self.ram.fetch(self.address, self.operand_size)
                self.registers.put(self.register_names['S'], operand, self.operand_size)
            elif self.opcode in self.JUMP_OPCODES:
                self.registers.put(self.register_names['ADDR'], self.address, self.address_size)

    def execute(self):
        """Add specific commands: conditional jumps and cmp."""
        if self.opcode == self.OPCODES['comp']:
            summator = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.alu.sub()
            self.registers.put(self.register_names['S'], summator, self.operand_size)
        else:
            if self.opcode in self.JUMP_OPCODES:
                self.execute_jump()
            else:
                if self.opcode in {self.OPCODES['load'], self.OPCODES['store']}:
                    pass
                else:
                    if self.opcode == self.OPCODES['swap']:
                        self.alu.swap()
                    else:
                        super().execute()

    def write_back(self):
        """Write result back."""
        if self.opcode == self.OPCODES['store']:
            value = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.ram.put(self.address, value, self.operand_size)


class ControlUnitM(ControlUnit):
    __doc__ = 'Control unit for address modification model machine.'
    address = 0
    register1 = ''
    register2 = ''
    register_names = {'PC': 'PC', 'ADDR': 'ADDR', 'RI': 'RI', 
     'R1': 'S', 'R2': 'RZ', 'S': 'S', 'RES': 'RZ', 
     'FLAGS': 'FLAGS'}
    REGISTER_OPCODES = {
     ControlUnit.OPCODES['radd'],
     ControlUnit.OPCODES['rsub'],
     ControlUnit.OPCODES['rsmul'],
     ControlUnit.OPCODES['rsdivmod'],
     ControlUnit.OPCODES['rumul'],
     ControlUnit.OPCODES['rudivmod'],
     ControlUnit.OPCODES['rmove'],
     ControlUnit.OPCODES['rcomp']}
    ARITHMETIC_OPCODES = ControlUnit.ARITHMETIC_OPCODES | {
     ControlUnit.OPCODES['radd'],
     ControlUnit.OPCODES['rsub'],
     ControlUnit.OPCODES['rsmul'],
     ControlUnit.OPCODES['rsdivmod'],
     ControlUnit.OPCODES['rumul'],
     ControlUnit.OPCODES['rudivmod']}

    def __init__(self, ir_size, *vargs, **kvargs):
        """See help(type(x))."""
        super().__init__(ir_size, *vargs, **kvargs)
        self.reg_addr_size = 4
        self.opcodes = self.ARITHMETIC_OPCODES | self.JUMP_OPCODES | self.REGISTER_OPCODES | {self.OPCODES['load'],
         self.OPCODES['store'],
         self.OPCODES['halt'],
         self.OPCODES['comp'],
         self.OPCODES['addr']}
        for reg in {'S', 'RZ', 'FLAGS', 'R0', 'R1', 'R2', 'R3', 'R4',
         'R5', 'R6', 'R7', 'R8', 'R9', 'RA', 'RB', 'RC',
         'RD', 'RE', 'RF'}:
            self.registers.add_register(reg, self.operand_size)

    def fetch_and_decode(self):
        """Fetch 3 addresses."""
        addr_mask = 2 ** self.address_size - 1
        reg_mask = 2 ** self.reg_addr_size - 1
        instruction_pointer = self.registers.fetch(self.register_names['PC'], self.address_size)
        batch_size = max(self.ram.word_size, self.OPCODE_SIZE)
        self.opcode = self.ram.fetch(instruction_pointer, batch_size)
        space_size = batch_size - self.OPCODE_SIZE
        self.opcode = Integer(self.opcode, batch_size, False)[space_size:].get_value()
        if self.opcode in self.opcodes - (self.REGISTER_OPCODES | {self.OPCODES['halt']}):
            instruction_size = self.OPCODE_SIZE + 2 * self.reg_addr_size + self.address_size
        else:
            instruction_size = self.OPCODE_SIZE + 2 * self.reg_addr_size
        instruction = self.fetch_instruction(instruction_size)
        if self.opcode in self.REGISTER_OPCODES:
            r_x = instruction >> self.reg_addr_size & reg_mask
            self.register1 = 'R' + hex(r_x).upper()[2:]
            r_y = instruction & reg_mask
            self.register2 = 'R' + hex(r_y).upper()[2:]
        elif self.opcode in self.opcodes - {self.OPCODES['halt']}:
            r_x = instruction >> self.reg_addr_size + self.address_size & reg_mask
            self.register1 = 'R' + hex(r_x).upper()[2:]
            modificator = 'R' + hex(instruction >> self.address_size & reg_mask).upper()[2:]
            if modificator != 'R0':
                modificator = self.registers.fetch(modificator, self.operand_size)
            else:
                modificator = 0
            self.address = instruction + modificator & addr_mask

    def load(self):
        """Load registers R1 and R2."""
        if self.opcode == self.OPCODES['store']:
            operand1 = self.registers.fetch(self.register1, self.operand_size)
            self.registers.put(self.register_names['R1'], operand1, self.operand_size)
        else:
            if self.opcode in self.REGISTER_OPCODES:
                operand1 = self.registers.fetch(self.register1, self.operand_size)
                self.registers.put(self.register_names['R1'], operand1, self.operand_size)
                operand2 = self.registers.fetch(self.register2, self.operand_size)
                self.registers.put(self.register_names['R2'], operand2, self.operand_size)
            else:
                if self.opcode in self.ARITHMETIC_OPCODES | {
                 self.OPCODES['comp'], self.OPCODES['load']}:
                    operand1 = self.registers.fetch(self.register1, self.operand_size)
                    self.registers.put(self.register_names['R1'], operand1, self.operand_size)
                    operand2 = self.ram.fetch(self.address, self.operand_size)
                    self.registers.put(self.register_names['R2'], operand2, self.operand_size)
                else:
                    if self.opcode == self.OPCODES['addr']:
                        self.registers.put(self.register_names['S'], self.address, self.operand_size)
                    elif self.opcode in self.JUMP_OPCODES:
                        self.registers.put(self.register_names['ADDR'], self.address, self.address_size)
        if self.opcode in self.REGISTER_OPCODES:
            self.opcode ^= 32

    def execute(self):
        """Add specific commands: conditional jumps and cmp."""
        if self.opcode == self.OPCODES['comp']:
            self.alu.sub()
        else:
            if self.opcode == self.OPCODES['load']:
                self.alu.move('R2', 'S')
            else:
                if self.opcode == self.OPCODES['store']:
                    self.alu.move('R1', 'S')
                else:
                    if self.opcode == self.OPCODES['addr']:
                        pass
                    else:
                        if self.opcode in self.JUMP_OPCODES:
                            self.execute_jump()
                        else:
                            super().execute()

    def write_back(self):
        """Write result back."""
        if self.opcode in self.ARITHMETIC_OPCODES | {self.OPCODES['load'],
         self.OPCODES['addr']}:
            value = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.registers.put(self.register1, value, self.operand_size)
            if self.opcode in self.DIVMOD_OPCODES:
                next_register = (int(self.register1[1:], 16) + 1) % 16
                next_register = 'R' + hex(next_register).upper()[2:]
                value = self.registers.fetch(self.register_names['RES'], self.operand_size)
                self.registers.put(next_register, value, self.operand_size)
        elif self.opcode == self.OPCODES['store']:
            value = self.registers.fetch(self.register_names['S'], self.operand_size)
            self.ram.put(self.address, value, self.operand_size)