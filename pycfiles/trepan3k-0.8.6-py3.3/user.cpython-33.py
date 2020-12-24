# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interfaces/user.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 5160 bytes
"""Interface when communicating with the user in the same process as
    the debugged program."""
import atexit, os, sys
from trepan import interface as Minterface
histfile = os.path.expanduser('~/.trepan3k_hist')
DEFAULT_USER_SETTINGS = {'histfile': histfile, 
 'complete': None}
try:
    from readline import read_history_file, set_completer, set_history_length
    from readline import write_history_file, parse_and_bind
except ImportError:
    pass

class UserInterface(Minterface.TrepanInterface):
    __doc__ = 'Interface when communicating with the user in the same\n    process as the debugged program.'

    def __init__(self, inp=None, out=None, opts={}):
        user_opts = DEFAULT_USER_SETTINGS.copy()
        user_opts.update(opts)
        from trepan.inout import input as Minput, output as Moutput
        atexit.register(self.finalize)
        self.interactive = True
        self.input = inp or Minput.DebuggerUserInput()
        self.output = out or Moutput.DebuggerUserOutput()
        if self.input.use_history():
            self.complete = user_opts['complete']
            if self.complete:
                parse_and_bind('tab: complete')
                set_completer(self.complete)
            self.histfile = user_opts['histfile']
            if self.histfile:
                try:
                    read_history_file(histfile)
                except IOError:
                    pass
                except:
                    return

                set_history_length(50)
                atexit.register(write_history_file, self.histfile)

    def close(self):
        """ Closes both input and output """
        self.input.close()
        self.output.close()

    def confirm--- This code section failed: ---

 L.  84         0  LOAD_FAST                'default'
                3  POP_JUMP_IF_FALSE    19  'to 19'

 L.  85         6  LOAD_FAST                'prompt'
                9  LOAD_STR                 '? (Y or n) '
               12  INPLACE_ADD      
               13  STORE_FAST               'prompt'
               16  JUMP_FORWARD         29  'to 29'
               19  ELSE                     '29'

 L.  87        19  LOAD_FAST                'prompt'
               22  LOAD_STR                 '? (N or y) '
               25  INPLACE_ADD      
               26  STORE_FAST               'prompt'
             29_0  COME_FROM            16  '16'

 L.  89        29  SETUP_LOOP          142  'to 142'

 L.  90        32  SETUP_EXCEPT         72  'to 72'

 L.  91        35  LOAD_FAST                'self'
               38  LOAD_ATTR                readline
               41  LOAD_FAST                'prompt'
               44  CALL_FUNCTION_1       1  '1 positional, 0 named'
               47  STORE_FAST               'reply'

 L.  92        50  LOAD_FAST                'reply'
               53  LOAD_ATTR                strip
               56  CALL_FUNCTION_0       0  '0 positional, 0 named'
               59  LOAD_ATTR                lower
               62  CALL_FUNCTION_0       0  '0 positional, 0 named'
               65  STORE_FAST               'reply'
               68  POP_BLOCK        
               69  JUMP_FORWARD         94  'to 94'
             72_0  COME_FROM_EXCEPT     32  '32'

 L.  93        72  DUP_TOP          
               73  LOAD_GLOBAL              EOFError
               76  COMPARE_OP               exception-match
               79  POP_JUMP_IF_FALSE    93  'to 93'
               82  POP_TOP          
               83  POP_TOP          
               84  POP_TOP          

 L.  94        85  LOAD_FAST                'default'
               88  RETURN_VALUE     
               89  POP_EXCEPT       
               90  JUMP_FORWARD         94  'to 94'
               93  END_FINALLY      
             94_0  COME_FROM            90  '90'
             94_1  COME_FROM            69  '69'

 L.  95        94  LOAD_FAST                'reply'
               97  LOAD_CONST               ('y', 'yes')
              100  COMPARE_OP               in
              103  POP_JUMP_IF_FALSE   110  'to 110'

 L.  96       106  LOAD_CONST               True
              109  RETURN_END_IF    

 L.  97       110  LOAD_FAST                'reply'
              113  LOAD_CONST               ('n', 'no')
              116  COMPARE_OP               in
              119  POP_JUMP_IF_FALSE   126  'to 126'

 L.  98       122  LOAD_CONST               False
              125  RETURN_END_IF    

 L. 100       126  LOAD_FAST                'self'
              129  LOAD_ATTR                msg
              132  LOAD_STR                 'Please answer y or n.'
              135  CALL_FUNCTION_1       1  '1 positional, 0 named'
              138  POP_TOP          

 L. 102       139  CONTINUE             32  'to 32'
            142_0  COME_FROM_LOOP       29  '29'

 L. 103       142  LOAD_FAST                'default'
              145  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 142

    def errmsg(self, msg, prefix='** '):
        """Common routine for reporting debugger error messages.
        """
        return self.msg('%s%s' % (prefix, msg))

    def finalize(self, last_wishes=None):
        try:
            self.msg("trepan3k: That's all, folks...")
            self.close()
        except IOError:
            pass

    def read_command(self, prompt=''):
        line = self.readline(prompt)
        return line

    def readline(self, prompt=''):
        if hasattr(self.input, 'use_raw'):
            if not self.input.use_raw and prompt and len(prompt) > 0:
                self.output.write(prompt)
                self.output.flush()
        return self.input.readline(prompt=prompt)


if __name__ == '__main__':
    intf = UserInterface()
    intf.errmsg('Houston, we have a problem here!')
    if len(sys.argv) > 1:
        try:
            line = intf.readline('Type something: ')
        except EOFError:
            print('No input EOF: ')
        else:
            print('You typed: %s' % line)
        line = intf.confirm('Are you sure', False)
        print('You typed: %s' % line)
        line = intf.confirm('Are you not sure', True)
        print('You typed: %s' % line)