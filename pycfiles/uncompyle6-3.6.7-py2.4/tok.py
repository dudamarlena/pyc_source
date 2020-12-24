# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/tok.py
# Compiled at: 2020-04-27 23:06:35
import re, sys
from uncompyle6 import PYTHON3
if PYTHON3:
    intern = sys.intern

def off2int(offset, prefer_last=True):
    if isinstance(offset, int):
        return offset
    else:
        assert isinstance(offset, str)
        offsets = list(map(int, offset.split('_')))
        if len(offsets) == 1:
            return offsets[0]
        else:
            assert len(offsets) == 2
            (offset_1, offset_2) = offsets
        if offset_1 + 2 == offset_2:
            if prefer_last:
                return offset_2
            else:
                return offset_1
        else:
            return offset_1


class Token:
    """
    Class representing a byte-code instruction.

    A byte-code token is equivalent to Python 3's dis.instruction or
    the contents of one line as output by dis.dis().
    """
    __module__ = __name__

    def __init__(self, opname, attr=None, pattr=None, offset=-1, linestart=None, op=None, has_arg=None, opc=None, has_extended_arg=False):
        self.kind = intern(opname)
        self.has_arg = has_arg
        self.attr = attr
        self.pattr = pattr
        if has_extended_arg:
            self.offset = '%d_%d' % (offset, offset + 2)
        else:
            self.offset = offset
        self.linestart = linestart
        if has_arg is False:
            self.attr = None
            self.pattr = None
        if opc is None:
            from xdis.std import _std_api
            self.opc = _std_api.opc
        else:
            self.opc = opc
        if op is None:
            self.op = self.opc.opmap.get(self.kind, None)
        else:
            self.op = op
        return

    def __eq__(self, o):
        """ '==' on kind and "pattr" attributes.
            It is okay if offsets and linestarts are different"""
        if isinstance(o, Token):
            return self.kind == o.kind and (self.pattr == o.pattr or self.attr == o.attr)
        else:
            return self.kind == o

    def __ne__(self, o):
        """ '!=', but it's okay if offsets and linestarts are different"""
        return not self.__eq__(o)

    def __repr__(self):
        return str(self.kind)

    def __str__(self):
        return self.format(line_prefix='')

    def format(self, line_prefix='', token_num=None):
        if token_num is not None:
            if self.linestart:
                prefix = '\n(%03d)%s L.%4d  ' % (token_num, line_prefix, self.linestart)
            else:
                prefix = '(%03d)%s' % (token_num, ' ' * (9 + len(line_prefix)))
        elif self.linestart:
            prefix = '\n%s L.%4d  ' % (line_prefix, self.linestart)
        else:
            prefix = ' ' * (9 + len(line_prefix))
        offset_opname = '%8s  %-17s' % (self.offset, self.kind)
        if not self.has_arg:
            return '%s%s' % (prefix, offset_opname)
        if isinstance(self.attr, int):
            argstr = '%6d ' % self.attr
        else:
            argstr = ' ' * 7
        name = self.kind
        if self.has_arg:
            pattr = self.pattr
            if self.opc:
                if self.op in self.opc.JREL_OPS:
                    if not self.pattr.startswith('to '):
                        pattr = 'to ' + self.pattr
                elif self.op in self.opc.JABS_OPS:
                    self.pattr = str(self.pattr)
                    if not self.pattr.startswith('to '):
                        pattr = 'to ' + str(self.pattr)
                elif self.op in self.opc.CONST_OPS:
                    if name == 'LOAD_STR':
                        pattr = self.attr
                    elif name == 'LOAD_CODE':
                        return '%s%s%s %s' % (prefix, offset_opname, argstr, pattr)
                    else:
                        return '%s%s        %r' % (prefix, offset_opname, pattr)
                elif self.op in self.opc.hascompare:
                    if isinstance(self.attr, int):
                        pattr = self.opc.cmp_op[self.attr]
                    return '%s%s%s %s' % (prefix, offset_opname, argstr, pattr)
                elif self.op in self.opc.hasvargs:
                    return '%s%s%s' % (prefix, offset_opname, argstr)
                elif name == 'LOAD_ASSERT':
                    return '%s%s        %s' % (prefix, offset_opname, pattr)
                elif self.op in self.opc.NAME_OPS:
                    if self.opc.version >= 3.0:
                        return '%s%s%s %s' % (prefix, offset_opname, argstr, self.attr)
                elif name == 'EXTENDED_ARG':
                    return '%s%s%s 0x%x << %s = %s' % (prefix, offset_opname, argstr, self.attr, self.opc.EXTENDED_ARG_SHIFT, pattr)
        elif re.search('_\\d+$', self.kind):
            return '%s%s%s' % (prefix, offset_opname, argstr)
        else:
            pattr = ''
        return '%s%s%s %r' % (prefix, offset_opname, argstr, pattr)

    def __hash__(self):
        return hash(self.kind)

    def __getitem__(self, i):
        raise IndexError

    def off2int(self, prefer_last=True):
        return off2int(self.offset, prefer_last)


NoneToken = Token('LOAD_CONST', offset=-1, attr=None, pattr=None)