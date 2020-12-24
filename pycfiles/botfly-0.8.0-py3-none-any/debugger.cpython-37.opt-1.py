# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /botfly/debugger.py
# Compiled at: 2019-11-10 21:53:48
# Size of source mod 2**32: 45263 bytes
"""Debugger that can be used instead of the pdb module.
"""
import sys, os, linecache, bdb, dis, code, re, inspect, traceback
from reprlib import Repr
from . import exceptions
from . import console
from . import controller
from . import parser
from . import ui
from . import commands
_repr = Repr()
_repr.maxstring = 200
_repr.maxother = 50
_saferepr = _repr.repr
DebuggerQuit = bdb.BdbQuit

def DEBUG(*args, **kwargs):
    """You can use this instead of 'print' when debugging. Prints to stderr.

    Emits nothing if run in "optimized" mode.
    """
    kwargs['file'] = sys.stderr
    print('DEBUG', *args, **kwargs)


def find_function(funcname, filename):
    cre = re.compile('def\\s+%s\\s*[(]' % funcname)
    try:
        fp = open(filename)
    except IOError:
        return
    else:
        lineno = 1
        answer = None
        while True:
            line = fp.readline()
            if line == '':
                break
            if cre.match(line):
                answer = (
                 funcname, filename, lineno)
                break
            lineno = lineno + 1

        fp.close()
        return answer


def lookupmodule(filename):
    """Helper function for break/clear parsing."""
    root, ext = os.path.splitext(filename)
    if ext == '':
        filename = filename + '.py'
    if os.path.isabs(filename):
        return filename
    for dirname in sys.path:
        while os.path.islink(dirname):
            dirname = os.readlink(dirname)

        fullname = os.path.join(dirname, filename)
        if os.path.exists(fullname):
            return fullname


def checkline--- This code section failed: ---

 L. 102         0  LOAD_GLOBAL              linecache
                2  LOAD_METHOD              getline
                4  LOAD_FAST                'filename'
                6  LOAD_FAST                'lineno'
                8  CALL_METHOD_2         2  '2 positional arguments'
               10  STORE_FAST               'line'

 L. 103        12  LOAD_FAST                'line'
               14  POP_JUMP_IF_TRUE     30  'to 30'

 L. 104        16  LOAD_FAST                'ui'
               18  LOAD_METHOD              print
               20  LOAD_STR                 '*** End of file'
               22  CALL_METHOD_1         1  '1 positional argument'
               24  POP_TOP          

 L. 105        26  LOAD_CONST               0
               28  RETURN_VALUE     
             30_0  COME_FROM            14  '14'

 L. 106        30  LOAD_FAST                'line'
               32  LOAD_METHOD              strip
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  STORE_FAST               'line'

 L. 108        38  LOAD_FAST                'line'
               40  POP_JUMP_IF_FALSE    86  'to 86'
               42  LOAD_FAST                'line'
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  LOAD_STR                 '#'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_TRUE     86  'to 86'
               54  LOAD_FAST                'line'
               56  LOAD_CONST               None
               58  LOAD_CONST               3
               60  BUILD_SLICE_2         2 
               62  BINARY_SUBSCR    
               64  LOAD_STR                 '"""'
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_TRUE     86  'to 86'
               70  LOAD_FAST                'line'
               72  LOAD_CONST               None
               74  LOAD_CONST               3
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_STR                 "'''"
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   100  'to 100'
             86_0  COME_FROM            68  '68'
             86_1  COME_FROM            52  '52'
             86_2  COME_FROM            40  '40'

 L. 109        86  LOAD_FAST                'ui'
               88  LOAD_METHOD              print
               90  LOAD_STR                 '*** Blank or comment'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_TOP          

 L. 110        96  LOAD_CONST               0
               98  RETURN_VALUE     
            100_0  COME_FROM            84  '84'

 L. 115       100  LOAD_FAST                'line'
              102  LOAD_CONST               None
              104  LOAD_CONST               3
              106  BUILD_SLICE_2         2 
              108  BINARY_SUBSCR    
              110  LOAD_STR                 'def'
              112  COMPARE_OP               ==
          114_116  POP_JUMP_IF_FALSE   330  'to 330'

 L. 116       118  LOAD_STR                 ''
              120  STORE_FAST               'instr'

 L. 117       122  LOAD_CONST               0
              124  STORE_FAST               'brackets'

 L. 118       126  SETUP_LOOP          330  'to 330'
            128_0  COME_FROM           322  '322'
            128_1  COME_FROM           310  '310'

 L. 119       128  LOAD_CONST               0
              130  STORE_FAST               'skipone'

 L. 120       132  SETUP_LOOP          248  'to 248'
              134  LOAD_FAST                'line'
              136  GET_ITER         
            138_0  COME_FROM           234  '234'
              138  FOR_ITER            246  'to 246'
              140  STORE_FAST               'c'

 L. 121       142  LOAD_FAST                'instr'
              144  POP_JUMP_IF_FALSE   184  'to 184'

 L. 122       146  LOAD_FAST                'skipone'
              148  POP_JUMP_IF_FALSE   156  'to 156'

 L. 123       150  LOAD_CONST               0
              152  STORE_FAST               'skipone'
              154  JUMP_ABSOLUTE       244  'to 244'
            156_0  COME_FROM           148  '148'

 L. 124       156  LOAD_FAST                'c'
              158  LOAD_STR                 '\\'
              160  COMPARE_OP               ==
              162  POP_JUMP_IF_FALSE   170  'to 170'

 L. 125       164  LOAD_CONST               1
              166  STORE_FAST               'skipone'
              168  JUMP_ABSOLUTE       244  'to 244'
            170_0  COME_FROM           162  '162'

 L. 126       170  LOAD_FAST                'c'
              172  LOAD_FAST                'instr'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   244  'to 244'

 L. 127       178  LOAD_STR                 ''
              180  STORE_FAST               'instr'
              182  JUMP_BACK           138  'to 138'
            184_0  COME_FROM           144  '144'

 L. 128       184  LOAD_FAST                'c'
              186  LOAD_STR                 '#'
              188  COMPARE_OP               ==
              190  POP_JUMP_IF_FALSE   196  'to 196'

 L. 129       192  BREAK_LOOP       
              194  JUMP_BACK           138  'to 138'
            196_0  COME_FROM           190  '190'

 L. 130       196  LOAD_FAST                'c'
              198  LOAD_CONST               ('"', "'")
              200  COMPARE_OP               in
              202  POP_JUMP_IF_FALSE   210  'to 210'

 L. 131       204  LOAD_FAST                'c'
              206  STORE_FAST               'instr'
              208  JUMP_BACK           138  'to 138'
            210_0  COME_FROM           202  '202'

 L. 132       210  LOAD_FAST                'c'
              212  LOAD_CONST               ('(', '{', '[')
              214  COMPARE_OP               in
              216  POP_JUMP_IF_FALSE   228  'to 228'

 L. 133       218  LOAD_FAST                'brackets'
              220  LOAD_CONST               1
              222  BINARY_ADD       
              224  STORE_FAST               'brackets'
              226  JUMP_BACK           138  'to 138'
            228_0  COME_FROM           216  '216'

 L. 134       228  LOAD_FAST                'c'
              230  LOAD_CONST               (')', '}', ']')
              232  COMPARE_OP               in
              234  POP_JUMP_IF_FALSE   138  'to 138'

 L. 135       236  LOAD_FAST                'brackets'
              238  LOAD_CONST               1
              240  BINARY_SUBTRACT  
              242  STORE_FAST               'brackets'
            244_0  COME_FROM           176  '176'
              244  JUMP_BACK           138  'to 138'
              246  POP_BLOCK        
            248_0  COME_FROM_LOOP      132  '132'

 L. 136       248  LOAD_FAST                'lineno'
              250  LOAD_CONST               1
              252  BINARY_ADD       
              254  STORE_FAST               'lineno'

 L. 137       256  LOAD_GLOBAL              linecache
              258  LOAD_METHOD              getline
              260  LOAD_FAST                'filename'
              262  LOAD_FAST                'lineno'
              264  CALL_METHOD_2         2  '2 positional arguments'
              266  STORE_FAST               'line'

 L. 138       268  LOAD_FAST                'line'
          270_272  POP_JUMP_IF_TRUE    288  'to 288'

 L. 139       274  LOAD_FAST                'ui'
              276  LOAD_METHOD              print
              278  LOAD_STR                 '*** end of file'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          

 L. 140       284  LOAD_CONST               0
              286  RETURN_VALUE     
            288_0  COME_FROM           270  '270'

 L. 141       288  LOAD_FAST                'line'
              290  LOAD_METHOD              strip
              292  CALL_METHOD_0         0  '0 positional arguments'
              294  STORE_FAST               'line'

 L. 142       296  LOAD_FAST                'line'
          298_300  POP_JUMP_IF_TRUE    304  'to 304'

 L. 143       302  CONTINUE            128  'to 128'
            304_0  COME_FROM           298  '298'

 L. 144       304  LOAD_FAST                'brackets'
              306  LOAD_CONST               0
              308  COMPARE_OP               <=
              310  POP_JUMP_IF_FALSE   128  'to 128'
              312  LOAD_FAST                'line'
              314  LOAD_CONST               0
              316  BINARY_SUBSCR    
              318  LOAD_CONST               ('#', '"', "'")
              320  COMPARE_OP               not-in
              322  POP_JUMP_IF_FALSE   128  'to 128'

 L. 145       324  BREAK_LOOP       
              326  JUMP_BACK           128  'to 128'
              328  POP_BLOCK        
            330_0  COME_FROM_LOOP      126  '126'
            330_1  COME_FROM           114  '114'

 L. 146       330  LOAD_FAST                'lineno'
              332  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 332


def run_editor(fname, lineno):
    if 'DISPLAY' in os.environ:
        if 'XEDITOR' in os.environ:
            ed = os.environ['XEDITOR']
        else:
            ed = os.environ.get('EDITOR', '/bin/vi')
    else:
        ed = os.environ.get('EDITOR', '/bin/vi')
    cmd = '%s +%d "%s"' % (ed, lineno, fname)
    os.system(cmd)


def _print_exception(ui, ex, prefix=''):
    ui.printf('{}%R{}%N: {}\n'.format(prefix, type(ex).__name__, ex))
    orig = ex
    while ex.__context__ is not None:
        ex = ex.__context__
        _print_exception(ui, ex, prefix=' While handling: ')

    ex = orig
    while ex.__cause__ is not None:
        ex = ex.__cause__
        _print_exception(ui, ex, prefix='    Raised from: ')


def _get_coroutine_stack(coro):
    """Extracts a list of stack frames from a chain of generator/coroutine
    calls.
    """
    frames = []
    while coro:
        if hasattr(coro, 'cr_frame'):
            f = coro.cr_frame
            coro = coro.cr_await
        else:
            if hasattr(coro, 'ag_frame'):
                f = coro.ag_frame
                coro = coro.ag_await
            else:
                if hasattr(coro, 'gi_frame'):
                    f = coro.gi_frame
                    coro = coro.gi_yieldfrom
                else:
                    f = None
                    coro = None
        if f is not None:
            frames.append(f)

    return frames


def _coroutine_format_stack(coro, complete=False):
    """Formats a traceback from a stack of coroutines/generators.
    """
    dirname = os.path.dirname(__file__)
    extracted_list = []
    checked = set()
    for f in _get_coroutine_stack(coro):
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        name = co.co_name
        if not complete:
            if os.path.dirname(filename) == dirname:
                continue
        if filename not in checked:
            checked.add(filename)
            linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        extracted_list.append((filename, lineno, name, line))

    if not extracted_list:
        resp = 'No stack for %r' % coro
    else:
        resp = 'Stack for %r (most recent call last):\n' % coro
        resp += ''.join(traceback.format_list(extracted_list))
    return resp


def _coroutine_where(coro):
    dirname = os.path.dirname(__file__)
    for f in _get_coroutine_stack(coro):
        lineno = f.f_lineno
        co = f.f_code
        filename = co.co_filename
        if os.path.dirname(filename) == dirname:
            continue
        return (
         filename, lineno)

    return (None, None)


class Debugger(bdb.Bdb):

    def __init__(self, skip=None, io=None):
        super().__init__(skip)
        self._io = io or console.ConsoleIO()
        self._ui = None
        self.tb_lineno = {}
        self._stack_stack = []
        self.forget()

    def reset(self):
        super().reset()
        self.forget()
        self._parser = None
        if self._ui is None:
            self._ui = ui.UserInterface(self._io)
            self._ui.register_expansion('S', self._expansions)

    def _expansions(self, c):
        if c == 'S':
            return '%s/%s' % (self.curindex + 1, len(self.stack))

    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None
        self.curexception = None
        self.tb_lineno.clear()

    def setup(self, f, t, exception=None):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, t)
        self.curframe = self.stack[self.curindex][0]
        self.curexception = exception
        while t:
            lineno = lasti2lineno(t.tb_frame.f_code, t.tb_lasti)
            self.tb_lineno[t.tb_frame] = lineno
            t = t.tb_next

    def push_traceback(self, f, t, exception=None):
        self._stack_stack.append((self.stack, self.curindex, self.curframe, self.curexception))
        self.setup(f, t, exception)

    def pop_traceback(self):
        try:
            val = self._stack_stack.pop()
        except IndexError:
            return False
        else:
            self.stack, self.curindex, self.curframe, self.curexception = val
            return True

    def set_trace(self, header=None, frame=None, start=0):
        """Start debugging from `frame`, or `start` frames back from
        caller's frame.
        If frame is not specified, debugging starts from caller's frame.
        """
        if header is not None:
            self._ui.print(header)
        if frame is None:
            frame = sys._getframe().f_back
        self.reset()
        if start:
            start = int(start)
            while start > 0 and frame:
                frame = frame.f_back
                start -= 1

        while frame:
            frame.f_trace = self.trace_dispatch
            self.botframe = frame
            frame = frame.f_back

        self.set_step()
        sys.settrace(self.trace_dispatch)

    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self.stop_here(frame):
            self._ui.printf('%g--Call--%N\n')
            self.interaction(frame, None)

    def message(self, message):
        self._ui.print(message)

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        self.interaction(frame, None)

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        frame.f_locals['__return__'] = return_value
        self._ui.printf('%g--return-->%N {}\n'.format(_saferepr(return_value)))
        self.interaction(frame, None)

    def user_exception--- This code section failed: ---

 L. 340         0  LOAD_FAST                'exc_tuple'
                2  UNPACK_SEQUENCE_3     3 
                4  STORE_FAST               'exc_type'
                6  STORE_FAST               'exc_value'
                8  STORE_FAST               'exc_traceback'

 L. 341        10  LOAD_FAST                'exc_type'
               12  LOAD_FAST                'exc_value'
               14  BUILD_TUPLE_2         2 
               16  LOAD_FAST                'frame'
               18  LOAD_ATTR                f_locals
               20  LOAD_STR                 '__exception__'
               22  STORE_SUBSCR     

 L. 342        24  LOAD_FAST                'exc_traceback'
               26  POP_JUMP_IF_TRUE     40  'to 40'
               28  LOAD_FAST                'exc_type'
               30  LOAD_GLOBAL              StopIteration
               32  COMPARE_OP               is
               34  POP_JUMP_IF_FALSE    40  'to 40'
               36  LOAD_STR                 'Internal '
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            34  '34'
             40_1  COME_FROM            26  '26'
               40  LOAD_STR                 ''
             42_0  COME_FROM            38  '38'
               42  STORE_FAST               'prefix'

 L. 343        44  LOAD_FAST                'self'
               46  LOAD_METHOD              print_exc
               48  LOAD_FAST                'prefix'
               50  LOAD_FAST                'exc_value'
               52  CALL_METHOD_2         2  '2 positional arguments'
               54  POP_TOP          

 L. 344        56  LOAD_FAST                'self'
               58  LOAD_METHOD              interaction
               60  LOAD_FAST                'frame'
               62  LOAD_FAST                'exc_traceback'
               64  LOAD_FAST                'exc_value'
               66  CALL_METHOD_3         3  '3 positional arguments'
               68  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 40_1

    def interaction(self, frame, traceback, exception=None):
        self.setup(frame, traceback, exception)
        self.print_stack_entry(self.stack[self.curindex])
        if self._parser is None:
            cmd = DebuggerCommands((self._ui), debugger=self, aliases=_DEFAULT_ALIASES)
            ctl = controller.CommandController(cmd)
            parser = DebuggerParser(ctl)
            self._parser = parser
        self._parser.interact()
        self.forget()

    def execline(self, line):
        locals = self.curframe.f_locals
        globals = self.curframe.f_globals
        try:
            code = compile(line + '\n', '<stdin>', 'single')
        except:
            t, v = sys.exc_info()[:2]
            self._ui.printf('*** Could not compile: %%r%s%%N: %s\n' % (t.__name__, v))
        else:
            try:
                exec(code, globals, locals)
            except:
                t, v = sys.exc_info()[:2]
                self._ui.printf('*** %%r%s%%N: %s\n' % (t.__name__, v))

    def go_up(self):
        if self.curindex == 0:
            return '*** Oldest frame'
        self.curindex = self.curindex - 1
        self.curframe = self.stack[self.curindex][0]
        self.print_stack_entry(self.stack[self.curindex])
        self.lineno = None

    def go_down(self):
        if self.curindex + 1 == len(self.stack):
            return '*** Newest frame'
        self.curindex = self.curindex + 1
        self.curframe = self.stack[self.curindex][0]
        self.print_stack_entry(self.stack[self.curindex])
        self.lineno = None

    def cause(self, exception=None):
        exc = exception or self.curexception
        if exc is None:
            self._ui.printf('%yNo current exception.%N\n')
            return False
        exc = exc.__cause__
        if exc is None:
            self._ui.printf('%yNo cause exception.%N\n')
            return False
        self.print_exc('Cause:', exc)
        self.push_traceback(exc.__traceback__.tb_frame, exc.__traceback__, exc)
        return True

    def switch_context(self, exception=None):
        exc = exception or self.curexception
        if exc is None:
            self._ui.printf('%yNo current exception.%N\n')
            return False
        exc = exc.__context__
        if exc is None:
            self._ui.printf('%yNo context exception.%N\n')
            return False
        self.print_exc('Context:', exc)
        self.push_traceback(exc.__traceback__.tb_frame, exc.__traceback__, exc)
        return True

    def getval(self, arg):
        return eval(arg, self.curframe.f_globals, self.curframe.f_locals)

    def retval(self):
        if '__return__' in self.curframe.f_locals:
            return self.curframe.f_locals['__return__']
        return

    def lineinfo(self, identifier):
        failed = (None, None, None)
        idstring = identifier.split("'")
        if len(idstring) == 1:
            id = idstring[0].strip()
        else:
            if len(idstring) == 3:
                id = idstring[1].strip()
            else:
                return failed
        if id == '':
            return failed
        parts = id.split('.')
        if parts[0] == 'self':
            del parts[0]
            if len(parts) == 0:
                return failed
        fname = self.curframe.f_code.co_filename
        if len(parts) == 1:
            item = parts[0]
        else:
            f = lookupmodule(parts[0])
            if f:
                fname = f
            item = parts[1]
        answer = find_function(item, fname)
        return answer or failed

    def print_stack_trace(self):
        try:
            for frame_lineno in self.stack:
                self.print_stack_entry(frame_lineno)

        except KeyboardInterrupt:
            pass

    def print_stack_entry(self, frame_lineno):
        frame, lineno = frame_lineno
        if frame is self.curframe:
            self._ui.print((self._ui.prompt_format('%I>%N')), end='')
        else:
            self._ui.print(' ', end='')
        self._ui.print(self.format_stack_entry(frame_lineno))
        self.lineno = None

    def format_stack_entry(self, frame_lineno):
        frame, lineno = frame_lineno
        filename = self.canonic(frame.f_code.co_filename)
        s = []
        s.append(self._ui.prompt_format('%y{}%N(%Y{!r}%N) in '.format(filename, lineno)))
        if frame.f_code.co_name:
            s.append(frame.f_code.co_name)
        else:
            s.append('<lambda>')
        if '__args__' in frame.f_locals:
            args = frame.f_locals['__args__']
            s.append(_saferepr(args))
        else:
            s.append('()')
        if '__return__' in frame.f_locals:
            rv = frame.f_locals['__return__']
            s.append(self._ui.prompt_format('%I->%N'))
            s.append(_saferepr(rv))
        line = linecache.getline(filename, lineno)
        if line:
            s.append('\n  ')
            s.append(line.strip())
        return ''.join(s)

    def print_exc(self, prefix, val):
        _print_exception((self._ui), val, prefix=prefix)

    def debug(self, arg):
        sys.settrace(None)
        globals = self.curframe.f_globals
        locals = self.curframe.f_locals
        p = Debugger(io=(self._io))
        p.reset()
        sys.call_tracing(p.run, (arg, globals, locals))
        sys.settrace(p.trace_dispatch)

    def debug_script(self, filename):
        import __main__
        __main__.__dict__.clear()
        __main__.__dict__.update({'__name__':'__main__',  '__file__':filename, 
         '__builtins__':__builtins__})
        self.mainpyfile = self.canonic(filename)
        try:
            with open(filename, 'rb') as (fp):
                code = compile(fp.read(), self.mainpyfile, 'exec')
        except SyntaxError as serr:
            try:
                self._ui.printf('%RSyntaxError%N: {}\n'.format(serr))
                return 2
            finally:
                serr = None
                del serr

        try:
            self.run(code)
        except SystemExit:
            es = sys.exc_info()[1]
            self._ui.printf('\n** %WThe program exited via sys.exit()%N. Exit status: {}\n'.format(es))
            return es
        except:
            ex, val, t = sys.exc_info()
            self.print_exc('debug_script:', val)
            self.interaction(t.tb_frame, t, val)
            return 99


def lasti2lineno(code, lasti):
    linestarts = list(dis.findlinestarts(code))
    linestarts.reverse()
    for i, lineno in linestarts:
        if lasti >= i:
            return lineno

    return 0


class DebuggerParser(parser.CommandParser):

    def initialize(self):
        ANY = ui.ANY
        f = ui.FSM(0)
        f.arg = ''
        f.add_default_transition(self._error, 0)
        f.add_transition(ANY, 0, self._addtext, 0)
        f.add_transitions(' \t', 0, self._wordbreak, 0)
        f.add_transition('\n', 0, self._doit, 0)
        f.add_transition('\\', 0, None, 1)
        f.add_transition(ANY, 1, self._slashescape, 0)
        f.add_transition('$', 0, self._startvar, 7)
        f.add_transition('{', 7, self._vartext, 9)
        f.add_transitions(self.VARCHARS, 7, self._vartext, 7)
        f.add_transition(ANY, 7, self._endvar, 0)
        f.add_transition('}', 9, self._endvar, 0)
        f.add_transition(ANY, 9, self._vartext, 9)
        self._fsm = f


class DebuggerCommands(commands.BaseCommands):

    def __init__(self, ui, debugger, aliases):
        super().__init__(ui, aliases=aliases)
        self._obj = debugger

    def _reset_namespace(self):
        self._namespace = self._obj.curframe.f_locals

    def finalize(self):
        self._ui.environ['SHLVL'] -= 1
        if not self._obj.pop_traceback():
            self._obj.set_quit()

    def clone(self):
        return self.__class__((self._ui), (self._obj), aliases=(self._aliases))

    def default_command(self, arguments):
        """If not a debugger command, evaluate it as a statement."""
        line = ' '.join(arguments['argv'])
        self._obj.execline(line)

    def execute(self, arguments):
        """Execute <statement> in current frame context.

        Usage:
            execute <statement>...
        """
        line = ' '.join(arguments['argv'][1:])
        self._obj.execline(line)

    def python(self, arguments):
        """Enter an interactive interpreter in the current frame.

        Usage:
            python
        """
        ns = self._obj.curframe.f_globals.copy()
        ns.update(self._obj.curframe.f_locals)
        console = code.InteractiveConsole(locals=ns, filename=(self._obj.curframe.f_code.co_filename))
        console.raw_input = self._ui.user_input
        try:
            saveps1, saveps2 = sys.ps1, sys.ps2
        except AttributeError:
            saveps1, saveps2 = ('>>> ', '... ')

        sys.ps1, sys.ps2 = ('%GPython%N:%S> ', 'more> ')
        try:
            console.interact(banner='You are now in Python. ^D exits.', exitmsg='Resuming debugger.')
        finally:
            sys.ps1, sys.ps2 = saveps1, saveps2

    def brk(self, arguments):
        """Set a break point.

        Usage:
            brk [-t] [([<file>:]<lineno> | <function>)] [, <condition>...]

        With a line number argument, set a break there in the current
        file.  With a function name, set a break at first executable line
        of that function.  Without argument, list all breaks.  If a second
        argument is present, it is a string specifying an expression
        which must evaluate to true before the breakpoint is honored.

        The line number may be prefixed with a filename and a colon,
        to specify a breakpoint in another file (probably one that
        hasn't been loaded yet).  The file is searched for on sys.path;
        the .py suffix may be omitted.
        """
        temporary = arguments['-t']
        if not arguments['<lineno>']:
            if self._obj.breaks:
                self._ui.print('Num Type         Disp Enb   Where')
                for bp in bdb.Breakpoint.bpbynumber:
                    if bp:
                        bp.bpprint()

            else:
                return
                filename = None
                lineno = None
                if arguments['<condition>']:
                    cond = ' '.join(arguments['<condition>'])
                else:
                    cond = None
            lineno = arguments['<lineno>']
            colon = lineno.rfind(':')
            if colon >= 0:
                filename = lineno[:colon].rstrip()
                f = lookupmodule(filename)
                if not f:
                    self._ui.print('*** ', repr(filename), 'not found from sys.path')
                    return
            else:
                filename = f
                lineno = lineno[colon + 1:].lstrip()
                try:
                    lineno = int(lineno)
                except ValueError as msg:
                    try:
                        self._ui.print('*** Bad lineno:', lineno, msg)
                        return
                    finally:
                        msg = None
                        del msg

        else:
            try:
                lineno = int(lineno)
            except ValueError:
                try:
                    func = eval(lineno, self._obj.curframe.f_globals, self._obj.curframe.f_locals)
                except:
                    func = lineno

                try:
                    if hasattr(func, '__func__'):
                        func = func.__func__
                    code = func.__code__
                    lineno = code.co_firstlineno
                    filename = code.co_filename
                except:
                    ok, filename, ln = self._obj.lineinfo(lineno)
                    if not ok:
                        self._ui.print('*** The specified object', repr(lineno))
                        self._ui.print('is not a function or was not found along sys.path.')
                        return
                    lineno = int(ln)

            if not filename:
                filename = self.curframe.f_code.co_filename
            line = checkline(filename, lineno, self._ui)
        if line:
            err = self._obj.set_break(filename, line, temporary, cond)
            if err:
                self._ui.error(str(err))
            else:
                bp = self._obj.get_breaks(filename, line)[(-1)]
                self._ui.print('Breakpoint %d at %s:%d' % (bp.number, bp.file, bp.line))
        else:
            self._ui.warning('Bad line number, or function not found.')

    def enable(self, arguments):
        """Enables the breakpoints given.

        Usage:
            enable <bpnumber>...
        """
        for i in arguments['<bpnumber>']:
            try:
                i = int(i)
            except ValueError:
                self._ui.print('Breakpoint index %r is not a number' % i)
                continue

            if not 0 <= i < len(bdb.Breakpoint.bpbynumber):
                self._ui.print('No breakpoint numbered', i)
                continue
            bp = bdb.Breakpoint.bpbynumber[i]
            if bp:
                bp.enable()

    def disable(self, arguments):
        """Disables the breakpoints.

        Disable all given break points.

        Usage:
            disable <bpnumber>...
        """
        for i in arguments['<bpnumber>']:
            try:
                i = int(i)
            except ValueError:
                self._ui.print('Breakpoint index %r is not a number' % i)
                continue

            if not 0 <= i < len(bdb.Breakpoint.bpbynumber):
                self._ui.print('No breakpoint numbered', i)
                continue
            bp = bdb.Breakpoint.bpbynumber[i]
            if bp:
                bp.disable()

    def condition(self, arguments):
        """Conditional breakpoint.

        Usage:
            condition <bpnumber> [<condition>]

        The <condition> is a string specifying an expression which
        must evaluate to true before the breakpoint is honored.
        If <condition> is absent, any existing condition is removed;
        i.e., the breakpoint is made unconditional.
        """
        bpnum = int(arguments['bpnumber'])
        cond = arguments['<condition>']
        bp = bdb.Breakpoint.bpbynumber[bpnum]
        if bp:
            bp.cond = cond
            if not cond:
                self._ui.print('Breakpoint', bpnum, 'is now unconditional.')

    def ignore(self, arguments):
        """Sets the ignore count for the given breakpoint number.

        A breakpoint becomes active when the ignore count is zero.  When
        non-zero, the count is decremented each time the breakpoint is reached
        and the breakpoint is not disabled and any associated condition
        evaluates to true.

        Usage:
            ignore <bpnumber> [<count>]
    """
        bpnum = int(arguments['bpnumber'])
        count = int(arguments['<count>'] or 0)
        bp = bdb.Breakpoint.bpbynumber[bpnum]
        if bp:
            bp.ignore = count
            if count > 0:
                reply = 'Will ignore next '
                if count > 1:
                    reply = reply + '%d crossings' % count
                else:
                    reply = reply + '1 crossing'
                self._ui.print(reply + ' of breakpoint %d.' % bpnum)
            else:
                self._ui.print('Will stop next time breakpoint', bpnum, 'is reached.')

    def clear(self, arguments):
        """Clear breakpoints.

        Three possibilities, tried in this order:
        clear -> clear all breaks, ask for confirmation
        clear file:lineno -> clear all breaks at file:lineno
        clear bpno bpno ... -> clear breakpoints by number

        With a space separated list of breakpoint numbers, clear
        those breakpoints.  Without argument, clear all breaks (but
        first ask confirmation).  With a filename:lineno argument,
        clear all breaks at that line in that file.

        Usage:
            clear
            clear <file:lineno>
            clear <breakpoint>...
        """
        if not arguments['<file:lineno>']:
            if not arguments['<breakpoint>']:
                if self._ui.yes_no('Clear all breaks? '):
                    self._obj.clear_all_breaks()
                return
        else:
            arg = arguments['<file:lineno>']
            if arg:
                if ':' in arg:
                    i = arg.rfind(':')
                    filename = arg[:i]
                    arg = arg[i + 1:]
                    try:
                        lineno = int(arg)
                    except ValueError:
                        err = 'Invalid line number (%s)' % arg
                    else:
                        err = self._obj.clear_break(filename, lineno)
                    if err:
                        self._ui.error('clear break: {}'.format(err))
            else:
                err = self._obj.clear_bpbynumber(i)
                if err:
                    self._ui.error('clear breakpoint: {}'.format(err))
            return
        for i in arguments['<breakpoint>']:
            err = self._obj.clear_bpbynumber(i)
            if err:
                self._ui.error('clear breakpoint: {}'.format(err))
            else:
                self._ui.print('Deleted breakpoint %s ' % (i,))

    def where(self, arguments):
        """Print a stack trace, with the most recent frame at the bottom.

        An arrow indicates the "current frame", which determines the
        context of most commands.  'bt' is an alias for this command.
        """
        self._obj.print_stack_trace()

    backtrace = where

    def up(self, arguments):
        """Move the current frame one level up in the stack trace
        (to a newer frame).
        """
        res = self._obj.go_up()
        if res:
            self._ui.print(res)
        self._reset_namespace()

    def down(self, arguments):
        """Move the current frame one level down in the stack trace
        (to an older frame).
        """
        res = self._obj.go_down()
        if res:
            self._ui.print(res)
        self._reset_namespace()

    def step(self, arguments):
        """Execute the current line, stop at the first possible occasion
        (either in a function that is called or in the current function).
        """
        self._obj.set_step()
        raise exceptions.CommandExit()

    def next(self, arguments):
        """Continue execution until the next line in the current function
        is reached or it returns.
        """
        self._obj.set_next(self._obj.curframe)
        raise exceptions.CommandExit()

    def returns(self, arguments):
        """Continue execution until the current function returns."""
        self._obj.set_return(self._obj.curframe)
        raise exceptions.CommandExit()

    def cont(self, arguments):
        """Continue execution, only stop when a breakpoint is encountered."""
        self._obj.set_continue()
        if self._obj.breaks:
            raise exceptions.CommandExit()
        else:
            self._obj._parser = None
            raise exceptions.CommandQuit()

    def switch(self, arguments):
        """Switch to the context exception.

        If the current exception was raised inside another exception handler,
        switch to that context for debugging.
        """
        if self._obj.switch_context():
            self._reset_namespace()
            raise exceptions.NewCommand(self.clone())

    def cause(self, arguments):
        """Switch to the original exception.

        If the current exception being handled was raised from another, switch
        to the from exception traceback.
        """
        if self._obj.cause():
            self._reset_namespace()
            raise exceptions.NewCommand(self.clone())

    def debug(self, arguments):
        """Enter a recursive debugger.

        Steps through the code argument (which is an arbitrary expression or
        statement to be executed in the current environment).

        Usage:
            debug <statement>
        """
        self._ui.print('=== entering recursive debugger')
        self._ui.environ['SHLVL'] += 1
        self._obj.debug(' '.join(arguments['argv'][1:]))
        self._ui.print('=== leaving recursive debugger')

    def quit(self, arguments):
        super(DebuggerCommands, self).exit(arguments)

    def args(self, arguments):
        """Print the arguments of the current function."""
        f = self._obj.curframe
        arginfo = inspect.getargvalues(f)
        self._ui.print(f.f_code.co_name, inspect.formatargvalues((arginfo.args), (arginfo.varargs),
          (arginfo.keywords), (arginfo.locals), formatvalue=(lambda value: '=' + _saferepr(value))))

    def retval(self, arguments):
        """Show return value."""
        val = self._obj.retval()
        self._ui.print(_saferepr(val))

    def exception(self, arguments):
        """Show the currently debugged exception."""
        if self._obj.curexception is not None:
            self._obj.print_exc('Current exception:', self._obj.curexception)
        else:
            self._ui.print('No current exception set.')

    def show(self, arguments):
        """Shows the current frame's object and values.

        If parameter names are given then show only those local names.

        Usage:
            show [<name>...]
        """
        f = self._obj.curframe
        args = arguments['<name>']
        if args:
            for name in args:
                try:
                    self._ui.print('%25.25s = %s' % (name, _saferepr(f.f_locals[name])))
                except KeyError:
                    self._ui.print('%r not found.' % (name,))

        else:
            args, varargs, varkw, local = inspect.getargvalues(f)
            self._ui.printf('%I{}%N (\n'.format(f.f_code.co_name or '<lambda>'))
            for name in args:
                val = local.get(name, '*** no formal ***')
                self._ui.print('%15.15s = %s,' % (name, _saferepr(val)))

            if varargs is not None:
                val = local.get(varargs, '*** no formal ***')
                self._ui.print('%15.15s = %s,' % ('*' + varargs, _saferepr(val)))
            if varkw is not None:
                val = local.get(varkw, '*** no formal ***')
                self._ui.print('%15.15s = %s,' % ('**' + varkw, _saferepr(val)))
            self._ui.print('  )')
            nargs = len(args) + (1 if varargs is not None else 0) + (1 if varkw is not None else 0)
            s = []
            for localname in f.f_code.co_varnames[nargs:]:
                val = local.get(localname, '*** unassigned ***')
                s.append('%15.15s = %s' % (localname, _saferepr(val)))

            if s:
                self._ui.print('  Compiled locals:')
                self._ui.print('\n'.join(s))
            local = local.copy()
            for localname in f.f_code.co_varnames:
                local.pop(localname, None)

        if local:
            self._ui.print('  Extra locals:')
            for name, val in local.items():
                self._ui.print('%15.15s = %s' % (name, _saferepr(val)))

    def print(self, arguments):
        """Print the value of the expression in the current frame.

        Usage:
            print <expression>...
        """
        expression = ' '.join(arguments['argv'][1:])
        try:
            self._ui.print(repr(self._obj.getval(expression)))
        except:
            ex = sys.exc_info()[1]
            _print_exception(self._ui, ex)

    def info(self, arguments):
        """Print information about the current frame's code.

        Usage:
            info
        """
        f = self._obj.curframe
        self._ui.print(dis.code_info(f.f_code))

    def disassemble(self, arguments):
        """Print op codes for the current frame.

        Usage:
            disassemble
        """
        f = self._obj.curframe
        bc = dis.Bytecode((f.f_code), current_offset=(f.f_lasti))
        self._ui.print(bc.dis())

    def list(self, arguments):
        """List source code for the current file.

        Without arguments, list 20 lines around the current line or continue the
        previous listing.  With one argument, list 20 lines centered at that
        line.  With two arguments, list the given range; if the second argument
        is less than the first, it is a count.

        Usage:
            list [<first> [<last>]]
        """
        last = arguments['<last>']
        first = arguments['<first>']
        if first is not None:
            first = max(1, int(first))
            if last is not None:
                last = int(last)
                if last < first:
                    last = first + last
        elif self._obj.lineno is None:
            first = max(1, self._obj.curframe.f_lineno - 10)
        else:
            first = self._obj.lineno + 1
        if last is None:
            last = first + 20
        filename = self._obj.curframe.f_code.co_filename
        self._print_source(filename, first, last)

    def edit(self, arguments):
        """Open your editor at the current location."""
        line = self._obj.curframe.f_lineno
        filename = self._obj.curframe.f_code.co_filename
        run_editor(filename, line)

    def whatis(self, arguments):
        """Prints the type of the argument.

        Usage:
            whatis <name>...
        """
        arg = ' '.join(arguments['argv'][1:])
        try:
            value = eval(arg, self._obj.curframe.f_globals, self._obj.curframe.f_locals)
        except:
            v = sys.exc_info()[1]
            self._ui.printf('*** %R{}%N: {}\n'.format(type(v).__name__, v))
            return
        else:
            if inspect.ismodule(value):
                self._ui.print(str(value))
            else:
                if inspect.isasyncgenfunction(value):
                    self._ui.print('Async Gen function:', value.__name__, inspect.signature(value))
                else:
                    if inspect.isasyncgen(value):
                        self._ui.print('Async Gen:', value.__name__, inspect.signature(value))
                    else:
                        if inspect.iscoroutine(value):
                            self._ui.print('Coroutine:', value)
                            self._ui.print('    state:', inspect.getcoroutinestate(value))
                            if inspect.isawaitable(value):
                                self._ui.print('  and awaitable.')
                                self._ui.print('  stack:', _coroutine_format_stack(value, complete=False))
                        elif inspect.isgenerator(value):
                            self._ui.print('Generator:', value)
                            self._ui.print('    state:', inspect.getgeneratorstate(value))
                            if inspect.isawaitable(value):
                                self._ui.print('  and awaitable.')
                        elif inspect.iscoroutinefunction(value):
                            self._ui.print('Coroutine function:', value.__name__, inspect.signature(value))
                        else:
                            if inspect.isgeneratorfunction(value):
                                self._ui.print('Generator function:', value.__name__, inspect.signature(value))
                            else:
                                if inspect.isfunction(value):
                                    self._ui.print('Function:', value.__name__, inspect.signature(value))
                                else:
                                    if inspect.ismethod(value):
                                        self._ui.print('Method:', value.__name__, inspect.signature(value))
                                    else:
                                        if inspect.iscode(value):
                                            self._ui.print('Code object:', value.co_name)
                                        else:
                                            if inspect.isclass(value):
                                                self._ui.print('Class:', value.__name__)
                                            else:
                                                if inspect.ismethoddescriptor(value):
                                                    self._ui.print('Method descriptor:', value.__name__)
                                                else:
                                                    if inspect.isdatadescriptor(value):
                                                        self._ui.print('Data descriptor:', value.__name__)
                                                    else:
                                                        self._ui.print(repr(type(value)))

    def search(self, arguments):
        """Search the source file for the regular expression pattern.

        Usage:
            search <pattern>...
    """
        patt = re.compile(' '.join(arguments['argv'][1:]))
        filename = self._obj.curframe.f_code.co_filename
        if self._obj.lineno is None:
            start = 0
        else:
            start = max(0, self._obj.lineno - 9)
        lines = linecache.getlines(filename)[start:]
        for lineno, line in enumerate(lines):
            mo = patt.search(line)
            if mo:
                self._print_source(filename, lineno + start - 10, lineno + start + 10)
                return
        else:
            self._ui.print('Pattern not found.')

    def _print_source(self, filename, first, last):
        breaklist = self._obj.get_file_breaks(filename)
        curframe = self._obj.curframe
        try:
            for lineno in range(first, last + 1):
                line = linecache.getline(filename, lineno)
                if not line:
                    self._ui.printf('%Y[EOF]%N\n')
                    break
                else:
                    s = []
                    s.append('%5.5s%s' % (lineno,
                     self._ui.prompt_format(' %RB%N') if lineno in breaklist else '  '))
                    if lineno == curframe.f_lineno:
                        s.append(self._ui.prompt_format('%I->%N '))
                    else:
                        if self._obj.tb_lineno.get(curframe, 0) == lineno:
                            s.append(self._ui.prompt_format('%I>>%N '))
                        else:
                            s.append('   ')
                    self._ui.print(''.join(s), line.rstrip())
                    self._obj.lineno = lineno

        except KeyboardInterrupt:
            pass


_DEFAULT_ALIASES = {'p':[
  'print'], 
 'l':[
  'list'], 
 'n':[
  'next'], 
 's':[
  'step'], 
 'c':[
  'cont'], 
 'ret':[
  'returns'], 
 'dis':[
  'disassemble'], 
 'r':[
  'returns'], 
 'u':[
  'up'], 
 'd':[
  'down'], 
 'exec':[
  'execute'], 
 'e':[
  'execute'], 
 'bp':[
  'brk'], 
 'break':[
  'brk'], 
 'bt':[
  'where'], 
 'q':[
  'quit'], 
 '/':[
  'search']}

def run(statement, globals=None, locals=None):
    Debugger().run(statement, globals, locals)


def runeval(expression, globals=None, locals=None):
    return Debugger().runeval(expression, globals, locals)


def runcall(*args):
    return (Debugger().runcall)(*args)


def set_trace(*, header=None, frame=None, start=0):
    Debugger().set_trace(header=header, frame=frame, start=start)


def post_mortem(t=None):
    """Start debugging at the given traceback."""
    exc = val = None
    if t is None:
        exc, val, t = sys.exc_info()
    elif t is None:
        raise ValueError('A valid traceback must be passed if no exception is being handled')
    else:
        p = Debugger()
        p.reset()
        while t.tb_next is not None:
            t = t.tb_next

        if exc and val:
            p.print_exc('Post Mortem Exception: ', val)
        else:
            exc, val, _ = sys.exc_info()
            del _
            if exc is None:
                DEBUG('No active exception!')
            else:
                p.print_exc('Active Exception:', val)
    p.interaction(t.tb_frame, t, val)


def pm():
    post_mortem(sys.last_traceback)


def from_exception(ex, io=None):
    """Start debugging from the place of the given exception instance."""
    tb = ex.__traceback__
    p = Debugger(io=io)
    p.reset()
    while tb.tb_next is not None:
        tb = tb.tb_next

    p.print_exc('', ex)
    p.interaction(tb.tb_frame, tb, ex)


def debug(method, *args, **kwargs):
    """Run the method and debug any exception, except syntax or user
    interrupt.
    """
    try:
        method(*args, **kwargs)
    except:
        ex, val, tb = sys.exc_info()
        if ex in (SyntaxError, IndentationError, KeyboardInterrupt):
            sys.__excepthook__(ex, val, tb)
        else:
            from_exception(val)


def debugger_hook(exc, value, tb):
    if hasattr(sys.stderr, 'isatty'):
        if not sys.stderr.isatty() or exc in (SyntaxError,
         IndentationError,
         KeyboardInterrupt):
            sys.__excepthook__(exc, value, tb)
    else:
        from_exception(value)


def autodebug(on=True):
    """Enables this debugger for all uncaught exceptions."""
    if on:
        sys.excepthook = debugger_hook
    else:
        sys.excepthook = sys.__excepthook__


def debug_script(filename):
    db = Debugger()
    db.reset()
    sys.path[0] = os.path.dirname(filename)
    return db.debug_script(filename)


sys.excepthook = sys.__excepthook__