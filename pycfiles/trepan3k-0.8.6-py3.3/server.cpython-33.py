# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interfaces/server.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 4861 bytes
"""Module for Server (i.e. program to communication-device) interaction"""
import atexit
from trepan import interface as Minterface
from trepan.inout import tcpserver as Mtcpserver, fifoserver as Mfifoserver
from trepan.interfaces import comcodes as Mcomcodes
DEFAULT_INIT_CONNECTION_OPTS = {'IO': 'TCP',  'PORT': 1955}

class ServerInterface(Minterface.TrepanInterface):
    __doc__ = 'Interface for debugging a program but having user control\n    reside outside of the debugged process, possibly on another\n    computer.'

    def __init__(self, inout=None, out=None, connection_opts={}):
        atexit.register(self.finalize)
        opts = DEFAULT_INIT_CONNECTION_OPTS.copy()
        opts.update(connection_opts)
        self.inout = None
        if inout:
            self.inout = inout
        else:
            self.server_type = opts['IO']
            if 'FIFO' == self.server_type:
                self.inout = Mfifoserver.FIFOServer()
            else:
                self.inout = Mtcpserver.TCPServer(opts=opts)
        self.output = self.inout
        self.input = self.inout
        self.interactive = True
        self.histfile = None
        return

    def close(self):
        """ Closes both input and output """
        if self.inout:
            self.inout.close()

    def confirm--- This code section failed: ---

 L.  64         0  SETUP_LOOP          123  'to 123'

 L.  65         3  SETUP_EXCEPT         53  'to 53'

 L.  66         6  LOAD_FAST                'self'
                9  LOAD_ATTR                write_confirm
               12  LOAD_FAST                'prompt'
               15  LOAD_FAST                'default'
               18  CALL_FUNCTION_2       2  '2 positional, 0 named'
               21  POP_TOP          

 L.  67        22  LOAD_FAST                'self'
               25  LOAD_ATTR                readline
               28  LOAD_STR                 ''
               31  CALL_FUNCTION_1       1  '1 positional, 0 named'
               34  LOAD_ATTR                strip
               37  CALL_FUNCTION_0       0  '0 positional, 0 named'
               40  LOAD_ATTR                lower
               43  CALL_FUNCTION_0       0  '0 positional, 0 named'
               46  STORE_FAST               'reply'
               49  POP_BLOCK        
               50  JUMP_FORWARD         75  'to 75'
             53_0  COME_FROM_EXCEPT      3  '3'

 L.  68        53  DUP_TOP          
               54  LOAD_GLOBAL              EOFError
               57  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    74  'to 74'
               63  POP_TOP          
               64  POP_TOP          
               65  POP_TOP          

 L.  69        66  LOAD_FAST                'default'
               69  RETURN_VALUE     
               70  POP_EXCEPT       
               71  JUMP_FORWARD         75  'to 75'
               74  END_FINALLY      
             75_0  COME_FROM            71  '71'
             75_1  COME_FROM            50  '50'

 L.  70        75  LOAD_FAST                'reply'
               78  LOAD_CONST               ('y', 'yes')
               81  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE    91  'to 91'

 L.  71        87  LOAD_CONST               True
               90  RETURN_END_IF    

 L.  72        91  LOAD_FAST                'reply'
               94  LOAD_CONST               ('n', 'no')
               97  COMPARE_OP               in
              100  POP_JUMP_IF_FALSE   107  'to 107'

 L.  73       103  LOAD_CONST               False
              106  RETURN_END_IF    

 L.  75       107  LOAD_FAST                'self'
              110  LOAD_ATTR                msg
              113  LOAD_STR                 'Please answer y or n.'
              116  CALL_FUNCTION_1       1  '1 positional, 0 named'
              119  POP_TOP          

 L.  77       120  CONTINUE              3  'to 3'
            123_0  COME_FROM_LOOP        0  '0'

 L.  78       123  LOAD_FAST                'default'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 123

    def errmsg(self, str, prefix='** '):
        """Common routine for reporting debugger error messages.
           """
        return self.msg('%s%s' % (prefix, str))

    def finalize(self, last_wishes=Mcomcodes.QUIT):
        if self.is_connected():
            self.inout.writeline(last_wishes)
        self.close()

    def is_connected(self):
        """ Return True if we are connected """
        return self.inout and 'connected' == self.inout.state

    def msg(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.inout.writeline(Mcomcodes.PRINT + msg)

    def msg_nocr(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will not have a newline added to it
        """
        self.inout.write(Mcomcodes.PRINT + msg)

    def read_command(self, prompt):
        return self.readline(prompt)

    def read_data(self):
        return self.inout.read_data()

    def readline(self, prompt, add_to_history=True):
        if prompt:
            self.write_prompt(prompt)
        coded_line = self.inout.read_msg()
        self.read_ctrl = coded_line[0]
        return coded_line[1:]

    def state(self):
        """ Return connected """
        return self.inout.state

    def write_prompt(self, prompt):
        return self.inout.writeline(Mcomcodes.PROMPT + prompt)

    def write_confirm(self, prompt, default):
        if default:
            code = Mcomcodes.CONFIRM_TRUE
        else:
            code = Mcomcodes.CONFIRM_FALSE
        return self.inout.writeline(code + prompt)


if __name__ == '__main__':
    connection_opts = {'IO': 'TCP',  'PORT': 1954}
    intf = ServerInterface(connection_opts=connection_opts)