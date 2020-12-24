# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/scanners/scanner36.py
# Compiled at: 2020-04-20 22:50:15
"""
Python 3.6 bytecode decompiler scanner

Does some additional massaging of xdis-disassembled instructions to
make things easier for decompilation.

This sets up opcodes Python's 3.6 and calls a generalized
scanner routine for Python 3.
"""
from uncompyle6.scanners.scanner3 import Scanner3
from xdis.opcodes import opcode_36 as opc
JUMP_OPS = opc.JUMP_OPS

class Scanner36(Scanner3):
    __module__ = __name__

    def __init__(self, show_asm=None, is_pypy=False):
        Scanner3.__init__(self, 3.6, show_asm, is_pypy)

    def ingest(self, co, classname=None, code_objects={}, show_asm=None):
        (tokens, customize) = Scanner3.ingest(self, co, classname, code_objects, show_asm)
        not_pypy36 = not (self.version == 3.6 and self.is_pypy)
        for t in tokens:
            if not_pypy36 and t.op == self.opc.CALL_FUNCTION_EX and t.attr & 1:
                t.kind = 'CALL_FUNCTION_EX_KW'
            elif t.op == self.opc.BUILD_STRING:
                t.kind = 'BUILD_STRING_%s' % t.attr
            elif t.op == self.opc.CALL_FUNCTION_KW:
                t.kind = 'CALL_FUNCTION_KW_%s' % t.attr
            elif t.op == self.opc.FORMAT_VALUE:
                if t.attr & 4:
                    t.kind = 'FORMAT_VALUE_ATTR'
            elif not_pypy36 and t.op == self.opc.BUILD_MAP_UNPACK_WITH_CALL:
                t.kind = 'BUILD_MAP_UNPACK_WITH_CALL_%d' % t.attr
            elif not_pypy36 and t.op == self.opc.BUILD_TUPLE_UNPACK_WITH_CALL:
                t.kind = 'BUILD_TUPLE_UNPACK_WITH_CALL_%d' % t.attr

        return (
         tokens, customize)


if __name__ == '__main__':
    from uncompyle6 import PYTHON_VERSION
    if PYTHON_VERSION == 3.6:
        import inspect
        co = inspect.currentframe().f_code
        (tokens, customize) = Scanner36().ingest(co)
        for t in tokens:
            print t.format()

    else:
        print 'Need to be Python 3.6 to demo; I am %s.' % PYTHON_VERSION