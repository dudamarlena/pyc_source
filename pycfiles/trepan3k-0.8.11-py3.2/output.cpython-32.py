# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/output.py
# Compiled at: 2015-05-14 22:21:52
"""Debugger output. """
import io, sys, types
from trepan.inout import base as Mbase

class DebuggerUserOutput(Mbase.DebuggerInOutBase):
    """Debugger output shown directly to what we think of as end-user
    ouptut as opposed to a relay mechanism to another process. Output
    could be an interactive terminal, but it might also be file output"""

    def __init__(self, out=None, opts=None):
        self.flush_after_write = False
        self.output = out or sys.stdout
        self.open(self.output, opts)

    def flush(self):
        return self.output.flush()

    def open--- This code section failed: ---

 L.  40         0  LOAD_GLOBAL              isinstance
                3  LOAD_FAST                'output'
                6  LOAD_GLOBAL              io
                9  LOAD_ATTR                TextIOWrapper
               12  CALL_FUNCTION_2       2  '2 positional, 0 named'
               15  POP_JUMP_IF_TRUE    118  'to 118'

 L.  41        18  LOAD_GLOBAL              isinstance
               21  LOAD_FAST                'output'
               24  LOAD_GLOBAL              io
               27  LOAD_ATTR                StringIO
               30  CALL_FUNCTION_2       2  '2 positional, 0 named'
               33  POP_JUMP_IF_TRUE    118  'to 118'

 L.  42        36  LOAD_FAST                'output'
               39  LOAD_GLOBAL              sys
               42  LOAD_ATTR                stdout
               45  COMPARE_OP               ==
             48_0  COME_FROM            33  '33'
             48_1  COME_FROM            15  '15'
               48  POP_JUMP_IF_FALSE    54  'to 54'

 L.  43        51  JUMP_FORWARD        118  'to 118'
               54  ELSE                     '118'

 L.  44        54  LOAD_GLOBAL              isinstance
               57  LOAD_FAST                'output'
               60  LOAD_STR                 'string'
               63  LOAD_ATTR                __class__
               66  CALL_FUNCTION_2       2  '2 positional, 0 named'
               69  POP_JUMP_IF_FALSE    90  'to 90'

 L.  45        72  LOAD_GLOBAL              open
               75  LOAD_FAST                'output'
               78  LOAD_STR                 'w'
               81  CALL_FUNCTION_2       2  '2 positional, 0 named'
               84  STORE_FAST               'output'
               87  JUMP_FORWARD        118  'to 118'
               90  ELSE                     '118'

 L.  47        90  LOAD_GLOBAL              IOError
               93  LOAD_STR                 'Invalid output type (%s) for %s'

 L.  48        96  LOAD_FAST                'output'
               99  LOAD_ATTR                __class__
              102  LOAD_ATTR                __name__
              105  LOAD_FAST                'output'
              108  BUILD_TUPLE_2         2 
              111  BINARY_MODULO    
              112  CALL_FUNCTION_1       1  '1 positional, 0 named'
              115  RAISE_VARARGS_1       1  'exception'
            118_0  COME_FROM            87  '87'
            118_1  COME_FROM            51  '51'

 L.  51       118  LOAD_FAST                'output'
              121  LOAD_FAST                'self'
              124  STORE_ATTR               output

Parse error at or near `POP_JUMP_IF_FALSE' instruction at offset 48

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'.
        """
        if self.output.closed:
            raise IOError('writing %s on a closed file' % msg)
        self.output.write(msg)
        if self.flush_after_write:
            self.flush()


if __name__ == '__main__':
    out = DebuggerUserOutput()
    out.writeline('Hello, world!')
    out.write('Hello')
    out.writeline(', again.')
    out.open(sys.stdout)
    out.flush_after_write = True
    out.write('Last hello')
    out.close()
    try:
        out.writeline("You won't see me")
    except ValueError:
        pass

    out.close()