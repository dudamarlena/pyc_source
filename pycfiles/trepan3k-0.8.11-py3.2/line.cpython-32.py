# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/line.py
# Compiled at: 2015-05-27 09:44:41
import inspect, os, re
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import file
from trepan import clifns as Mclifns, misc as Mmisc

def find_function--- This code section failed: ---

 L.  25         0  LOAD_GLOBAL              re
                3  LOAD_ATTR                compile
                6  LOAD_STR                 'def\\s+%s\\s*[(]'
                9  LOAD_GLOBAL              re
               12  LOAD_ATTR                escape
               15  LOAD_FAST                'funcname'
               18  CALL_FUNCTION_1       1  '1 positional, 0 named'
               21  BINARY_MODULO    
               22  CALL_FUNCTION_1       1  '1 positional, 0 named'
               25  STORE_FAST               'cre'

 L.  26        28  SETUP_EXCEPT         47  'to 47'

 L.  27        31  LOAD_GLOBAL              open
               34  LOAD_FAST                'filename'
               37  CALL_FUNCTION_1       1  '1 positional, 0 named'
               40  STORE_FAST               'fp'
               43  POP_BLOCK        
               44  JUMP_FORWARD         69  'to 69'
             47_0  COME_FROM_EXCEPT     28  '28'

 L.  28        47  DUP_TOP          
               48  LOAD_GLOBAL              IOError
               51  COMPARE_OP               exception-match
               54  POP_JUMP_IF_FALSE    68  'to 68'
               57  POP_TOP          
               58  POP_TOP          
               59  POP_TOP          

 L.  29        60  LOAD_CONST               None
               63  RETURN_VALUE     
               64  POP_EXCEPT       
               65  JUMP_FORWARD         69  'to 69'
               68  END_FINALLY      
             69_0  COME_FROM            65  '65'
             69_1  COME_FROM            44  '44'

 L.  31        69  LOAD_CONST               1
               72  STORE_FAST               'lineno'

 L.  32        75  LOAD_CONST               None
               78  STORE_FAST               'answer'

 L.  33        81  SETUP_LOOP          159  'to 159'

 L.  34        84  LOAD_FAST                'fp'
               87  LOAD_ATTR                readline
               90  CALL_FUNCTION_0       0  '0 positional, 0 named'
               93  STORE_FAST               'line'

 L.  35        96  LOAD_FAST                'line'
               99  LOAD_STR                 ''
              102  COMPARE_OP               ==
              105  POP_JUMP_IF_FALSE   112  'to 112'

 L.  36       108  BREAK_LOOP       
              109  JUMP_FORWARD        112  'to 112'
            112_0  COME_FROM           109  '109'

 L.  37       112  LOAD_FAST                'cre'
              115  LOAD_ATTR                match
              118  LOAD_FAST                'line'
              121  CALL_FUNCTION_1       1  '1 positional, 0 named'
              124  POP_JUMP_IF_FALSE   146  'to 146'

 L.  38       127  LOAD_FAST                'funcname'
              130  LOAD_FAST                'filename'
              133  LOAD_FAST                'lineno'
              136  BUILD_TUPLE_3         3 
              139  STORE_FAST               'answer'

 L.  39       142  BREAK_LOOP       
              143  JUMP_FORWARD        146  'to 146'
            146_0  COME_FROM           143  '143'

 L.  40       146  LOAD_FAST                'lineno'
              149  LOAD_CONST               1
              152  BINARY_ADD       
              153  STORE_FAST               'lineno'

 L.  41       156  CONTINUE             84  'to 84'
            159_0  COME_FROM_LOOP       81  '81'

 L.  42       159  LOAD_FAST                'fp'
              162  LOAD_ATTR                close
              165  CALL_FUNCTION_0       0  '0 positional, 0 named'
              168  POP_TOP          

 L.  43       169  LOAD_FAST                'answer'
              172  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 159


class InfoLine(Mbase_subcmd.DebuggerSubcommand):
    """**info line**

Show information about the current line

See also:
---------
`info program`, `info frame`"""
    min_abbrev = 2
    max_args = 0
    need_stack = True
    short_help = 'Show current-line information'

    def lineinfo(self, identifier):
        failed = (None, None, None)
        idstring = identifier.split("'")
        if len(idstring) == 1:
            ident = idstring[0].strip()
        else:
            if len(idstring) == 3:
                ident = idstring[1].strip()
            else:
                return failed
        if ident == '':
            return failed
        else:
            parts = ident.split('.')
            if parts[0] == 'self':
                del parts[0]
                if len(parts) == 0:
                    return failed
            fname = self.proc.defaultFile()
            if len(parts) == 1:
                item = parts[0]
            else:
                m, f = file.lookupmodule('.'.join(parts[1:]), self.debugger.mainpyfile, self.core.canonic)
                if f:
                    fname = f
                item = parts[(-1)]
            answer = find_function(item, fname)
            return answer or failed

    def run(self, args):
        """Current line number in source file"""
        if not self.proc.curframe:
            self.errmsg('No line number information available.')
            return
        if len(args) == 3:
            answer = self.lineinfo(args[2])
            if answer[0]:
                item, filename, lineno = answer
                if not os.path.isfile(filename):
                    filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
                self.msg('Line %s of "%s" <%s>' % (
                 lineno, filename, item))
            return
        filename = self.core.canonic_filename(self.proc.curframe)
        if not os.path.isfile(filename):
            filename = Mclifns.search_file(filename, self.core.search_path, self.main_dirname)
        filename = self.core.canonic_filename(self.proc.curframe)
        msg1 = 'Line %d of "%s"' % (inspect.getlineno(self.proc.curframe),
         self.core.filename(filename))
        msg2 = 'at instruction %d' % self.proc.curframe.f_lasti
        if self.proc.event:
            msg2 += ', %s event' % self.proc.event
        self.msg(Mmisc.wrapped_lines(msg1, msg2, self.settings['width']))
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    d, cp = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoLine(i)
    sub.run([])
    cp.curframe = inspect.currentframe()
    for width in (80, 200):
        sub.settings['width'] = width
        sub.run(['file.py', 'lines'])