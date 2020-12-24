# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rbertra/workspace/repos/github.com/IBM/microprobe/targets/riscv/isa/riscv-v2_2/../riscv-common/./isa.py
# Compiled at: 2020-04-15 12:18:51
"""
Docstring
"""
from __future__ import absolute_import
import os, six
from microprobe.code.address import Address, InstructionAddress
from microprobe.code.var import Variable, VariableArray
from microprobe.target.isa import GenericISA
from microprobe.utils.logger import get_logger
from microprobe.utils.misc import twocs_to_int
LOG = get_logger(__name__)
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_RISCV_PCREL_LABEL = 0

class RISCVISA(GenericISA):

    def __init__(self, name, descr, ins, regs, comparators, generators):
        super(RISCVISA, self).__init__(name, descr, ins, regs, comparators, generators)
        self._scratch_registers += [self.registers['X31'],
         self.registers['F7']]
        self._control_registers += [ reg for reg in self.registers.values() if reg.type.name == 'rm'
                                   ]

    def set_register(self, register, value, context):
        LOG.debug('Setting register: %s to value %d', register.name, value)
        instrs = []
        current_value = context.get_register_value(register)
        if context.register_has_value(value):
            present_reg = context.registers_get_value(value)[0]
            if present_reg.type.name != register.type.name:
                present_reg = None
        else:
            present_reg = None
        if register.type.name == 'freg':
            LOG.debug('FP register')
            if present_reg is not None:
                LOG.debug('Value already present')
                instr = self.new_instruction('FSGNJ.S_V0')
                instr.set_operands([register, present_reg, present_reg])
                instrs.append(instr)
            else:
                LOG.debug('Setting value to scratch and then move to FP register')
                instrs += self.set_register(self._scratch_registers[0], value, context)
                instr = self.new_instruction('FCVT.S.L_V0')
                instr.set_operands([self._scratch_registers[0], register])
                instrs.append(instr)
        elif register.type.name == 'ireg':
            LOG.debug('Integer register')
            value_highest = int((value & 18446726481523507200) >> 44)
            value_high = int((value & 17587891077120) >> 32)
            value_low = int((value & 4294963200) >> 12)
            value_lowest = int(value & 4095)
            if value == 0:
                LOG.debug('Zero value')
                addi = self.new_instruction('ADDI_V0')
                addi.set_operands([0, self.registers['X0'], register])
                instrs.append(addi)
            elif present_reg is not None:
                LOG.debug('Value already present')
                addi = self.new_instruction('ADDI_V0')
                addi.set_operands([0, present_reg, register])
                instrs.append(addi)
            elif current_value is not None and abs(value - current_value) < 4096:
                addi = self.new_instruction('ADDI_V0')
                addi.set_operands([value - current_value, register, register])
                instrs.append(addi)
            elif register == self._scratch_registers[0]:
                LOG.debug('This is the scratch register.')
                if value < -2147483648 or value >= 2147483647:
                    LOG.debug('This is the scratch register. Long path')
                    lui = self.new_instruction('LUI_V0')
                    lui.set_operands([value_highest, register])
                    instrs.append(lui)
                    addiw = self.new_instruction('ADDIW_V0')
                    if value_high >= 2047:
                        addiw.set_operands([2047, register, register])
                        instrs.append(addiw)
                        value_high = value_high - 2047
                    addiw.set_operands([value_high, register, register])
                    instrs.append(addiw)
                    slli = self.new_instruction('SLLI_V0')
                    slli.set_operands([8, register, register])
                    instrs.append(slli)
                    nvalue = int((value & 4278190080) >> 24)
                    addi = self.new_instruction('ADDI_V0')
                    addi.set_operands([nvalue, register, register])
                    instrs.append(addi)
                    slli = self.new_instruction('SLLI_V0')
                    slli.set_operands([8, register, register])
                    instrs.append(slli)
                    nvalue = int((value & 16711680) >> 16)
                    addi = self.new_instruction('ADDI_V0')
                    addi.set_operands([nvalue, register, register])
                    instrs.append(addi)
                    slli = self.new_instruction('SLLI_V0')
                    slli.set_operands([8, register, register])
                    instrs.append(slli)
                    nvalue = int((value & 65280) >> 8)
                    addi = self.new_instruction('ADDI_V0')
                    addi.set_operands([nvalue, register, register])
                    instrs.append(addi)
                    slli = self.new_instruction('SLLI_V0')
                    slli.set_operands([8, register, register])
                    instrs.append(slli)
                    nvalue = int(value & 255)
                    addi = self.new_instruction('ADDI_V0')
                    addi.set_operands([nvalue, register, register])
                    instrs.append(addi)
                else:
                    LOG.debug('This is the scratch register. Short path')
                    if value_lowest > 2047:
                        value_low = value_low + 1
                        value_lowest = value - (value_low << 12)
                    lui = self.new_instruction('LUI_V0')
                    lui.set_operands([value_low, register])
                    addiw = self.new_instruction('ADDIW_V0')
                    addiw.set_operands([value_lowest, register, register])
                    instrs.append(lui)
                    instrs.append(addiw)
            elif value < -2147483648 or value >= 2147483647:
                LOG.debug('Use scratch register. Long path')
                instrs.extend(self.set_register(register, value >> 32, context))
                instrs.extend(self.set_register(self._scratch_registers[0], value & 4294967295, context))
                slli = self.new_instruction('SLLI_V0')
                slli.set_operands([32, register, register])
                instrs.append(slli)
                and_inst = self.new_instruction('AND_V0')
                and_inst.set_operands([
                 register, self._scratch_registers[0], register])
                instrs.append(and_inst)
            elif value >= -2147483648 and value < 2147483647:
                LOG.debug('Short path')
                if value_lowest > 2047:
                    value_low = value_low + 1
                    value_lowest = value - (value_low << 12)
                lui = self.new_instruction('LUI_V0')
                lui.set_operands([value_low, register])
                addiw = self.new_instruction('ADDIW_V0')
                addiw.set_operands([value_lowest, register, register])
                instrs.append(lui)
                instrs.append(addiw)
            else:
                LOG.debug('Register: %s set to value %d', register.name, value)
                raise NotImplementedError
        else:
            LOG.debug('Register: %s set to value %d', register.name, value)
            raise NotImplementedError
        if len(instrs) > 0:
            return instrs
        else:
            return super(RISCVISA, self).set_register(register, value, context)

    def set_register_to_address(self, register, address, context, force_absolute=False, force_relative=False):
        global _RISCV_PCREL_LABEL
        instrs = []
        LOG.debug("Begin setting '%s' to address '%s'", register, address)
        if isinstance(address.base_address, Variable):
            LOG.debug('Base address is a Variable: %s', address.base_address)
            closest = context.get_closest_address_value(address)
            if context.register_has_value(address):
                present_reg = context.registers_get_value(address)[0]
                displacement = 0
                LOG.debug("Address already in register '%s'", present_reg)
            else:
                if closest is not None:
                    present_reg, taddress = closest
                    displacement = address.displacement - taddress.displacement
                    LOG.debug("Closest value '%s' found in '%s'", taddress, present_reg)
                    LOG.debug('Displacement needed: %s', displacement)
                elif context.register_has_value(Address(base_address=address.base_address)):
                    present_reg = context.registers_get_value(Address(base_address=address.base_address))[0]
                    displacement = address.displacement
                    LOG.debug("Base address '%s' found in '%s'", taddress, present_reg)
                    LOG.debug('Displacement needed: %s', displacement)
                else:
                    present_reg = None
                    displacement = None
                LOG.debug('Present_reg: %s', present_reg)
                LOG.debug('Displacement: %s', displacement)
                if present_reg is not None:
                    if displacement != 0 and abs(displacement) < 2048:
                        addi_ins = self.new_instruction('ADDI_V0')
                        addi_ins.set_operands([displacement, present_reg,
                         register])
                        instrs.append(addi_ins)
                        LOG.debug('Computing directly from context (short)')
                        return instrs
                    if present_reg != register:
                        or_ins = self.new_instruction('OR_V0')
                        or_ins.set_operands([present_reg, present_reg, register])
                        instrs.append(or_ins)
                    if displacement != 0:
                        instrs += self.add_to_register(register, displacement)
                    LOG.debug('Computing directly from context (long)')
                    return instrs
        if context.symbolic and not force_absolute and not force_relative:
            basename = address.base_address
            if not isinstance(address.base_address, str):
                basename = address.base_address.name
            _RISCV_PCREL_LABEL += 1
            lnum = _RISCV_PCREL_LABEL
            auipc_ins = self.new_instruction('AUIPC_V0')
            auipc_ins.operands()[1].set_value(register)
            auipc_ins.operands()[0].set_value('%%pcrel_hi(%s)' % basename, check=False)
            auipc_ins.set_label('%s_pcrel_%d' % (basename, lnum))
            instrs.append(auipc_ins)
            addi_ins = self.new_instruction('ADDI_V0')
            addi_ins.operands()[1].set_value(register)
            addi_ins.operands()[2].set_value(register)
            addi_ins.operands()[0].set_value('%%pcrel_lo(%s_pcrel_%d)' % (basename, lnum), check=False)
            instrs.append(addi_ins)
            if address.displacement != 0:
                instrs += self.add_to_register(register, address.displacement)
            LOG.debug('End Loading symbolic reference')
            return instrs
        else:
            raise NotImplementedError
            return

    def load(self, register, address, context):
        ldi = self.new_instruction('LD_V0')
        ldi.operands()[2].set_value(register)
        ldi.memory_operands()[0].set_address(address, context)
        return [ldi]

    def load_float(self, register, address, context):
        ldi = self.new_instruction('FLD_V0')
        ldi.operands()[2].set_value(register)
        ldi.memory_operands()[0].set_address(address, context)
        return [ldi]

    def store_float(self, register, address, context):
        std = self.new_instruction('FSD_V0')
        std.operands()[2].set_value(register)
        std.memory_operands()[0].set_address(address, context)
        return [std]

    def store_integer(self, register, address, length, context):
        if length == 64:
            stg = self.new_instruction('SD_V0')
            stg.operands()[2].set_value(register)
            stg.memory_operands()[0].set_address(address, context)
            return [
             stg]
        if length == 32:
            stg = self.new_instruction('SW_V0')
            stg.operands()[2].set_value(register)
            stg.memory_operands()[0].set_address(address, context)
            return [
             stg]
        raise NotImplementedError

    def set_register_bits(self, dummy_register, dummy_value, dummy_mask, dummy_shift, dummy_context):
        raise NotImplementedError

    def store_decimal(self, dummy_address, dummy_length, dummy_value, dummy_context):
        raise NotImplementedError

    @property
    def program_counter(self):
        raise NotImplementedError

    def branch_unconditional_relative(self, source, target):
        LOG.debug('Source: %s', source)
        LOG.debug('Target: %s', target)
        raise NotImplementedError

    def add_to_register(self, register, value):
        instrs = []
        if register.type.name == 'ireg' and isinstance(value, six.integer_types):
            if value > 0:
                while value > 2047:
                    addi = self.new_instruction('ADDI_V0')
                    addi.set_operands([2047, register, register])
                    instrs.append(addi)
                    value = value - 2047

            elif value < 0:
                while value < -2047:
                    addi = self.new_instruction('ADDI_V0')
                    addi.set_operands([-2047, register, register])
                    instrs.append(addi)
                    value = value + 2047

            if abs(value) != 0:
                addi = self.new_instruction('ADDI_V0')
                addi.set_operands([value, register, register])
                instrs.append(addi)
        else:
            raise NotImplementedError
        return instrs

    def compare_and_branch(self, val1, val2, cond, target, context):
        assert cond in ('<', '>', '!=', '=', '>=', '<=')
        instrs = []
        if isinstance(val1, int) and isinstance(val1, six.integer_types):
            raise NotImplementedError
        elif isinstance(val1, six.integer_types):
            instrs += self.set_register(self.scratch_registers[0], val1, context)
            val1 = self.scratch_registers[0]
        elif isinstance(val2, six.integer_types):
            instrs += self.set_register(self.scratch_registers[0], val2, context)
            val2 = self.scratch_registers[0]
        if isinstance(target, str):
            target = InstructionAddress(base_address=target)
        if cond == '>':
            cond = '<'
            val1, val2 = val2, val1
        if cond == '<=':
            cond = '>='
            val1, val2 = val2, val1
        if cond == '=':
            bc_ins = self.new_instruction('BEQ_V0')
        elif cond == '!=':
            bc_ins = self.new_instruction('BNE_V0')
        elif cond == '<':
            bc_ins = self.new_instruction('BLT_V0')
        elif cond == '>=':
            bc_ins = self.new_instruction('BGE_V0')
        else:
            raise NotImplementedError
        bc_ins.set_operands([target, val2, val1, 0])
        instrs.append(bc_ins)
        return instrs

    def nop(self):
        instr = self.new_instruction('ADDI_V0')
        instr.set_operands([0,
         self.target.registers['X0'],
         self.target.registers['X0']])
        return instr

    def negate_register(self, dummy_register, dummy_context):
        raise NotImplementedError

    @property
    def context_var(self):
        if self._context_var is None:
            self._context_var = VariableArray('%s_context_var' % self._name, 'uint8_t', 600)
        return self._context_var

    def set_context(self, variable=None, tmpl_path=None):
        """ """
        if tmpl_path is None:
            tmpl_path = _MODULE_DIR
        return super(RISCVISA, self).set_context(variable=variable, tmpl_path=tmpl_path)

    def get_context(self, variable=None, tmpl_path=None):
        """ """
        if tmpl_path is None:
            tmpl_path = _MODULE_DIR
        return super(RISCVISA, self).get_context(variable=variable, tmpl_path=tmpl_path)

    def normalize_asm(self, mnemonic, operands):
        """ """
        if mnemonic == 'FENCE':
            new_operands = []
            for operand in operands:
                value = 0
                if 'I' in operand:
                    value += 8
                if 'O' in operand:
                    value += 4
                if 'R' in operand:
                    value += 2
                if 'W' in operand:
                    value += 1
                new_operands.append(str(value))

            return (mnemonic, new_operands)
        return (mnemonic, operands)