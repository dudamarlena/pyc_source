# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/pyte/lib/python3.5/site-packages/pyte/backports.py
# Compiled at: 2016-04-20 01:44:29
# Size of source mod 2**32: 5281 bytes
import collections, dis, sys
_Instruction = collections.namedtuple('_Instruction', 'opname opcode arg argval argrepr offset starts_line is_jump_target')

class Instruction(_Instruction):
    __doc__ = 'Details for a bytecode operation\n\n       Defined fields:\n         opname - human readable name for operation\n         opcode - numeric code for operation\n         arg - numeric argument to operation (if any), otherwise None\n         argval - resolved arg value (if known), otherwise same as arg\n         argrepr - human readable description of operation argument\n         offset - start index of operation within bytecode sequence\n         starts_line - line started by this opcode (if any), otherwise None\n         is_jump_target - True if other code jumps to here, otherwise False\n    '

    def _disassemble(self, lineno_width=3, mark_as_current=False):
        """Format instruction details for inclusion in disassembly output

        *lineno_width* sets the width of the line number field (0 omits it)
        *mark_as_current* inserts a '-->' marker arrow as part of the line
        """
        fields = []
        if lineno_width:
            if self.starts_line is not None:
                lineno_fmt = '%%%dd' % lineno_width
                fields.append(lineno_fmt % self.starts_line)
            else:
                fields.append(' ' * lineno_width)
            if mark_as_current:
                fields.append('-->')
            else:
                fields.append('   ')
            if self.is_jump_target:
                fields.append('>>')
        else:
            fields.append('  ')
        fields.append(repr(self.offset).rjust(4))
        fields.append(self.opname.ljust(20))
        if self.arg is not None:
            fields.append(repr(self.arg).rjust(5))
            if self.argrepr:
                fields.append('(' + self.argrepr + ')')
        return ' '.join(fields).rstrip()


def _get_instructions_bytes(code, varnames=None, names=None, constants=None, cells=None, linestarts=None, line_offset=0):
    """Iterate over the instructions in a bytecode string.

    Generates a sequence of Instruction namedtuples giving the details of each
    opcode.  Additional information about the code's runtime environment
    (e.g. variable names, constants) can be specified using optional
    arguments.

    """
    labels = dis.findlabels(code)
    extended_arg = 0
    starts_line = None
    free = None
    n = len(code)
    i = 0
    while i < n:
        op = code[i]
        offset = i
        if linestarts is not None:
            starts_line = linestarts.get(i, None)
            if starts_line is not None:
                starts_line += line_offset
        is_jump_target = i in labels
        i = i + 1
        arg = None
        argval = None
        argrepr = ''
        if op >= dis.HAVE_ARGUMENT:
            arg = code[i] + code[(i + 1)] * 256 + extended_arg
            extended_arg = 0
            i = i + 2
            if op == dis.EXTENDED_ARG:
                extended_arg = arg * 65536
            argval = arg
            if op in dis.hasconst:
                argval, argrepr = dis._get_const_info(arg, constants)
            else:
                if op in dis.hasname:
                    argval, argrepr = dis._get_name_info(arg, names)
                else:
                    if op in dis.hasjrel:
                        argval = i + arg
                        argrepr = 'to ' + repr(argval)
                    else:
                        if op in dis.haslocal:
                            argval, argrepr = dis._get_name_info(arg, varnames)
                        else:
                            if op in dis.hascompare:
                                argval = dis.cmp_op[arg]
                                argrepr = argval
                            else:
                                if op in dis.hasfree:
                                    argval, argrepr = dis._get_name_info(arg, cells)
                                elif op in dis.hasnargs:
                                    argrepr = '%d positional, %d keyword pair' % (code[(i - 2)], code[(i - 1)])
            yield dis.Instruction(dis.opname[op], op, arg, argval, argrepr, offset, starts_line, is_jump_target)


def _get_const_info(const_index, const_list):
    """Helper to get optional details about const references

       Returns the dereferenced constant and its repr if the constant
       list is defined.
       Otherwise returns the constant index and its repr().
    """
    argval = const_index
    if const_list is not None:
        argval = const_list[const_index]
    return (
     argval, repr(argval))


def apply():
    dis._get_instructions_bytes = _get_instructions_bytes
    dis.Instruction = Instruction
    dis._get_const_info = _get_const_info