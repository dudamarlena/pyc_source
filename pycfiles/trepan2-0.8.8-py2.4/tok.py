# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/parse/tok.py
# Compiled at: 2017-10-27 23:34:05


class Token:
    """
    Class representing a token.
    kind: the kind of token, e.g. filename, number, other
    value: specific instance value, e.g. "/tmp/foo.c", or 5
    offset: byte offset from start of parse string
    """
    __module__ = __name__

    def __init__(self, kind, value=None, offset=None):
        self.offset = offset
        self.kind = kind
        self.value = value

    def __eq__(self, o):
        """ '==', but it's okay if offset is different"""
        if isinstance(o, Token):
            return self.kind == o.kind
        else:
            return self.kind == o

    def __repr__(self):
        return str(self.kind)

    def __repr1__(self, indent, sib_num=''):
        return self.format(line_prefix=indent, sib_num=sib_num)

    def __str__(self):
        return self.format(line_prefix='')

    def format(self, line_prefix='', sib_num=None):
        if sib_num:
            sib_num = '%d.' % sib_num
        else:
            sib_num = ''
        prefix = '%s%s' % (line_prefix, sib_num)
        offset_opname = '%5s %-10s' % (self.offset, self.kind)
        if not self.value:
            return '%s%s' % (prefix, offset_opname)
        return '%s%s %s' % (prefix, offset_opname, self.value)

    def __hash__(self):
        return hash(self.kind)

    def __getitem__(self, i):
        raise IndexError