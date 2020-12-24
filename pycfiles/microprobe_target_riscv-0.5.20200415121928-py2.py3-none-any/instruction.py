# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rbertra/workspace/repos/github.com/IBM/microprobe/targets/riscv/isa/riscv-v2_2/../riscv-common/./instruction.py
# Compiled at: 2020-03-29 13:02:20
"""
Docstring
"""
from __future__ import absolute_import, print_function
from six.moves import zip
from microprobe.code.ins import InstructionOperandValue
from microprobe.exceptions import MicroprobeArchitectureDefinitionError
from microprobe.target.isa.instruction import GenericInstructionType
from microprobe.target.isa.operand import OperandDescriptor, OperandImmRange
from microprobe.utils.logger import get_logger
from microprobe.utils.misc import getnextf, int_to_twocs, twocs_to_int
LOG = get_logger(__name__)
_7BITS_OPERAND_DESCRIPTOR = OperandDescriptor(OperandImmRange('dummy', 'dummy', 0, 128, 1, True, 0, [], 0), False, False)
_5BITS_OPERAND_DESCRIPTOR = OperandDescriptor(OperandImmRange('dummy', 'dummy', 0, 32, 1, True, 0, [], 0), False, False)

class RISCVInstruction(GenericInstructionType):
    """
    RISC-V Instruction Class
    """

    def __init__(self, name, mnemonic, opcode, descr, iformat, operands, ioperands, moperands, instruction_checks, target_checks):
        super(RISCVInstruction, self).__init__(name, mnemonic, opcode, descr, iformat, operands, ioperands, moperands, instruction_checks, target_checks)

    def assembly(self, args, dummy_dissabled_fields=None):
        assembly_str = super(RISCVInstruction, self).assembly(args, dissabled_fields=[
         'sb_imm7', 'sb_imm5',
         's_imm7', 's_imm5',
         'pred', 'succ'])

        def _get_value(cfield, base):
            try:
                value = [ arg for arg in args if arg.descriptor.type.name == self._operand_descriptors[cfield].type.name
                        ][0].value
                return self._operand_descriptors[cfield].type.representation(value)
            except KeyError:
                raise MicroprobeArchitectureDefinitionError("Unable to find sub-field '%s' for the '%s' field" % (
                 cfield, base))

        if assembly_str.find('sb_imm12') > 0:
            assert _get_value('sb_imm5', 'sb_imm12') == '0'
            value = _get_value('sb_imm7', 'sb_imm12')
            assembly_str = assembly_str.replace('sb_imm12', str(value))
        if assembly_str.find('s_imm12') > 0:
            assert _get_value('s_imm5', 's_imm12') == '0'
            value = _get_value('s_imm7', 's_imm12')
            assembly_str = assembly_str.replace('s_imm12', str(value))
        for field in ['pred', 'succ']:
            if assembly_str.find(field) < 0:
                continue
            value = int(_get_value(field, field))
            str_value = ''
            if value & 8:
                str_value += 'i'
            if value & 4:
                str_value += 'o'
            if value & 2:
                str_value += 'r'
            if value & 1:
                str_value += 'w'
            assembly_str = assembly_str.replace(field, str_value)
            if value == 0:
                print((assembly_str, field, value))

        return assembly_str

    def binary(self, args, asm_args=None):
        LOG.debug('Start specific RISC-V codification')
        fix_needed = False
        fix_fields = ['sb_imm5', 's_imm5']
        base_fields = ['sb_imm7', 's_imm7']
        for fix_field in fix_fields:
            if fix_field in [ field.name for field in self.format.fields ]:
                fix_needed = True
                break

        long_str = fix_needed or super(RISCVInstruction, self).binary(args, asm_args=asm_args)
        if not len(long_str) in (32, ):
            raise AssertionError(len(long_str))
            LOG.debug('End specific RISC-V codification')
            return long_str
        next_operand_value = getnextf(iter(args))
        newargs = []
        for op_descriptor, field in zip(list(self.operands.items()), self.format.fields):
            dummy_fieldname, op_descriptor = op_descriptor
            operand, dummy = op_descriptor
            LOG.debug('Field: %s', field)
            LOG.debug('Operand: %s', operand)
            if operand.constant and field.name not in fix_fields + base_fields:
                if field.default_show:
                    arg = next_operand_value()
                    newargs.append(arg)
                continue
            if field.name not in fix_fields + base_fields:
                LOG.debug('Not fixing field: %s', field.name)
                arg = next_operand_value()
                newargs.append(arg)
                continue
            if field.name in base_fields:
                arg = next_operand_value()
                value = int(arg.type.codification(arg.value))
                value_coded = int_to_twocs(value, 12)
                assert twocs_to_int(value_coded, 12) == value
                newarg = InstructionOperandValue(_7BITS_OPERAND_DESCRIPTOR)
                newarg.set_value((value_coded & 4064) >> 5)
                if field.name == 'sb_imm7':
                    sb_imm5_value = value_coded & 31
                elif field.name == 's_imm7':
                    s_imm5_value = value_coded & 31
                else:
                    raise NotImplementedError
                LOG.debug("Set field '%s' value: %s --> %s", field.name, value, (value_coded & 4064) >> 5)
                newargs.append(newarg)
            if field.name in fix_fields:
                newarg = InstructionOperandValue(_5BITS_OPERAND_DESCRIPTOR)
                if field.name == 'sb_imm5':
                    value_fixed = sb_imm5_value
                elif field.name == 's_imm5':
                    value_fixed = s_imm5_value
                else:
                    raise NotImplementedError(field.name)
                LOG.debug("Set field '%s' value: %s --> %s", field.name, value, value_fixed)
                newarg.set_value(value_fixed)
                newargs.append(newarg)

        LOG.debug('Args: %s, %s', args, newargs)
        long_str = super(RISCVInstruction, self).binary(newargs, asm_args=args)
        assert len(long_str) in (16, 32, 48), len(long_str)
        LOG.debug('End specific RISC-V codification')
        return long_str