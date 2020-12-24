# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/bwprocessor/main.py
# Compiled at: 2016-01-13 01:45:18
import inspect, linecache, sys, traceback, pyficache
from reprlib import Repr
from trepan import vprocessor as Mprocessor
from trepan import exception as Mexcept, misc as Mmisc
from trepan.lib import bytecode as Mbytecode, display as Mdisplay
from trepan.lib import thred as Mthread
from trepan.bwprocessor import location as Mlocation, msg as Mmsg

def get_stack(f, t, botframe, proc_obj=None):
    """Return a stack of frames which the debugger will use for in
    showing backtraces and in frame switching. As such various frame
    that are really around may be excluded unless we are debugging the
    sebugger. Also we will add traceback frame on top if that
    exists."""
    exclude_frame = lambda f: False
    if proc_obj:
        settings = proc_obj.debugger.settings
        if not settings['dbg_trepan']:
            exclude_frame = lambda f: proc_obj.core.ignore_filter.is_included(f)
    stack = []
    if t and t.tb_frame is f:
        t = t.tb_next
    while f is not None:
        if exclude_frame(f):
            break
        stack.append((f, f.f_lineno))
        f = f.f_back

    stack.reverse()
    i = max(0, len(stack) - 1)
    while t is not None:
        stack.append((t.tb_frame, t.tb_lineno))
        t = t.tb_next

    return (stack, i)


def run_hooks(obj, hooks, *args):
    """Run each function in `hooks' with args"""
    for hook in hooks:
        if hook(obj, *args):
            return True

    return False


def resolve_name(obj, command_name):
    if command_name not in obj.commands:
        return None
    else:
        return command_name


DEFAULT_PROC_OPTS = {'initfile_list': []}

class BWProcessor(Mprocessor.Processor):

    def __init__(self, core_obj, opts=None):
        Mprocessor.Processor.__init__(self, core_obj)
        self.response = {'errs': [],  'msg': []}
        self.continue_running = False
        self.cmd_instances = self._populate_commands()
        self.cmd_name = ''
        self.current_command = ''
        self.debug_nest = 1
        self.display_mgr = Mdisplay.DisplayMgr()
        self.intf = core_obj.debugger.intf
        self.last_command = None
        self.precmd_hooks = []
        self.preloop_hooks = []
        self.postcmd_hooks = []
        self._populate_cmd_lists()
        self.different_line = None
        self.curframe = None
        self.event = None
        self.event_arg = None
        self.frame = None
        self.list_lineno = 0
        self._repr = Repr()
        self._repr.maxstring = 100
        self._repr.maxother = 60
        self._repr.maxset = 10
        self._repr.maxfrozen = 10
        self._repr.array = 10
        self._saferepr = self._repr.repr
        self.stack = []
        self.thread_name = None
        self.frame_thread_name = None
        return

    def add_preloop_hook(self, hook, position=-1, nodups=True):
        if hook in self.preloop_hooks:
            return False
        self.preloop_hooks.insert(position, hook)
        return True

    def adjust_frame(self, pos, absolute_pos):
        """Adjust stack frame by pos positions. If absolute_pos then
        pos is an absolute number. Otherwise it is a relative number.

        A negative number indexes from the other end."""
        if not self.curframe:
            Mmsg.errmsg(self, 'No stack.')
            return
        else:
            if absolute_pos:
                if pos >= 0:
                    pos = len(self.stack) - pos - 1
                else:
                    pos = -pos - 1
            else:
                pos += self.curindex
            if pos < 0:
                Mmsg.errmsg(self, 'Adjusting would put us beyond the oldest frame.')
                return
            if pos >= len(self.stack):
                Mmsg.errmsg(self, 'Adjusting would put us beyond the newest frame.')
                return
            self.curindex = pos
            self.curframe = self.stack[self.curindex][0]
            self.print_location()
            self.list_lineno = None
            return

    def defaultFile(self):
        """Produce a reasonable default."""
        filename = self.curframe.f_code.co_filename
        if filename == '<string>' and self.debugger.mainpyfile:
            filename = self.debugger.mainpyfile
        return filename

    def event_processor(self, frame, event, event_arg, prompt='Trepan'):
        """command event processor: reading a commands do something with them."""
        self.frame = frame
        self.event = event
        self.event_arg = event_arg
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        line = linecache.getline(filename, lineno, frame.f_globals)
        if not line:
            opts = {'output': 'plain',  'reload_on_change': self.settings('reload'),  'strip_nl': False}
            line = pyficache.getline(filename, lineno, opts)
        self.current_source_text = line
        if self.settings('skip') is not None:
            if Mbytecode.is_def_stmt(line, frame):
                return True
            if Mbytecode.is_class_def(line, frame):
                return True
        self.thread_name = Mthread.current_thread_name()
        self.frame_thread_name = self.thread_name
        self.process_commands()
        return True

    def forget(self):
        """ Remove memory of state variables set in the command processor """
        self.stack = []
        self.curindex = 0
        self.curframe = None
        self.thread_name = None
        self.frame_thread_name = None
        return

    def eval(self, arg):
        """Eval string arg in the current frame context."""
        try:
            return eval(arg, self.curframe.f_globals, self.curframe.f_locals)
        except:
            t, v = sys.exc_info()[:2]
            if isinstance(t, str):
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            Mmsg.errmsg(self, str('%s: %s' % (exc_type_name, arg)))
            raise

        return

    def exec_line(self, line):
        if self.curframe:
            local_vars = self.curframe.f_locals
            global_vars = self.curframe.f_globals
        else:
            local_vars = None
            global_vars = None
        try:
            code = compile(line + '\n', '"%s"' % line, 'single')
            exec(code, global_vars, local_vars)
        except:
            t, v = sys.exc_info()[:2]
            if isinstance(t, bytes):
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            Mmsg.errmsg(self, '%s: %s' % (str(exc_type_name), str(v)))

        return

    def ok_for_running(self, cmd_obj, name, cmd_hash):
        """We separate some of the common debugger command checks here:
        whether it makes sense to run the command in this execution state,
        if the command has the right number of arguments and so on.
        """
        if hasattr(cmd_obj, 'execution_set'):
            if self.core.execution_status not in cmd_obj.execution_set:
                part1 = "Command '%s' is not available for execution status:" % name
                Mmsg.errmsg(self, Mmisc.wrapped_lines(part1, self.core.execution_status, self.debugger.settings['width']))
                return False
        if self.frame is None and cmd_obj.need_stack:
            self.intf[(-1)].errmsg("Command '%s' needs an execution stack." % name)
            return False
        else:
            return True

    def process_commands(self):
        """Handle debugger commands."""
        if self.core.execution_status != 'No program':
            self.setup()
            Mlocation.print_location(self, self.event)
        leave_loop = run_hooks(self, self.preloop_hooks)
        self.continue_running = False
        while not leave_loop:
            try:
                run_hooks(self, self.precmd_hooks)
                leave_loop = self.process_command()
                if leave_loop or self.continue_running:
                    break
            except EOFError:
                if len(self.debugger.intf) > 1:
                    del self.debugger.intf[-1]
                    self.last_command = ''
                else:
                    if self.debugger.intf[(-1)].output:
                        self.debugger.intf[(-1)].output.writeline('Leaving')
                        raise Mexcept.DebuggerQuit
                    break

        return run_hooks(self, self.postcmd_hooks)

    def process_command--- This code section failed: ---

 L. 320         0  BUILD_MAP_2           2  ''
                3  BUILD_LIST_0          0 
                6  LOAD_STR                 'errs'
                9  STORE_MAP        
               10  BUILD_LIST_0          0 
               13  LOAD_STR                 'msg'
               16  STORE_MAP        
               17  LOAD_FAST                'self'
               20  STORE_ATTR               response

 L. 321        23  LOAD_FAST                'self'
               26  LOAD_ATTR                intf
               29  LOAD_CONST               -1
               32  BINARY_SUBSCR    
               33  LOAD_ATTR                read_command
               36  CALL_FUNCTION_0       0  '0 positional, 0 named'
               39  STORE_FAST               'cmd_hash'

 L. 324        42  LOAD_GLOBAL              isinstance
               45  LOAD_FAST                'cmd_hash'
               48  LOAD_GLOBAL              dict
               51  CALL_FUNCTION_2       2  '2 positional, 0 named'
               54  POP_JUMP_IF_TRUE    114  'to 114'

 L. 325        57  LOAD_GLOBAL              Mmsg
               60  LOAD_ATTR                errmsg
               63  LOAD_FAST                'self'
               66  LOAD_STR                 'invalid input, expecting a hash: %s'
               69  LOAD_FAST                'cmd_hash'
               72  BINARY_MODULO    

 L. 326        73  BUILD_MAP_1           1  ''
               76  LOAD_CONST               True
               79  LOAD_STR                 'set_name'
               82  STORE_MAP        
               83  CALL_FUNCTION_3       3  '3 positional, 0 named'
               86  POP_TOP          

 L. 327        87  LOAD_FAST                'self'
               90  LOAD_ATTR                intf
               93  LOAD_CONST               -1
               96  BINARY_SUBSCR    
               97  LOAD_ATTR                msg
              100  LOAD_FAST                'self'
              103  LOAD_ATTR                response
              106  CALL_FUNCTION_1       1  '1 positional, 0 named'
              109  POP_TOP          

 L. 328       110  LOAD_CONST               False
              113  RETURN_END_IF    

 L. 329       114  LOAD_STR                 'command'
              117  LOAD_FAST                'cmd_hash'
              120  COMPARE_OP               not-in
              123  POP_JUMP_IF_FALSE   183  'to 183'

 L. 330       126  LOAD_GLOBAL              Mmsg
              129  LOAD_ATTR                errmsg
              132  LOAD_FAST                'self'

 L. 331       135  LOAD_STR                 "invalid input, expecting a 'command' key: %s"

 L. 332       138  LOAD_FAST                'cmd_hash'
              141  BINARY_MODULO    

 L. 333       142  BUILD_MAP_1           1  ''
              145  LOAD_CONST               True
              148  LOAD_STR                 'set_name'
              151  STORE_MAP        
              152  CALL_FUNCTION_3       3  '3 positional, 0 named'
              155  POP_TOP          

 L. 334       156  LOAD_FAST                'self'
              159  LOAD_ATTR                intf
              162  LOAD_CONST               -1
              165  BINARY_SUBSCR    
              166  LOAD_ATTR                msg
              169  LOAD_FAST                'self'
              172  LOAD_ATTR                response
              175  CALL_FUNCTION_1       1  '1 positional, 0 named'
              178  POP_TOP          

 L. 335       179  LOAD_CONST               False
              182  RETURN_END_IF    

 L. 337       183  LOAD_FAST                'cmd_hash'
              186  LOAD_STR                 'command'
              189  BINARY_SUBSCR    
              190  LOAD_FAST                'self'
              193  STORE_ATTR               cmd_name

 L. 338       196  LOAD_GLOBAL              resolve_name
              199  LOAD_FAST                'self'
              202  LOAD_FAST                'self'
              205  LOAD_ATTR                cmd_name
              208  CALL_FUNCTION_2       2  '2 positional, 0 named'
              211  STORE_FAST               'cmd_name'

 L. 339       214  LOAD_FAST                'cmd_name'
              217  POP_JUMP_IF_FALSE   410  'to 410'

 L. 340       220  LOAD_FAST                'self'
              223  LOAD_ATTR                commands
              226  LOAD_FAST                'cmd_name'
              229  BINARY_SUBSCR    
              230  STORE_FAST               'cmd_obj'

 L. 341       233  LOAD_FAST                'self'
              236  LOAD_ATTR                ok_for_running
              239  LOAD_FAST                'cmd_obj'
              242  LOAD_FAST                'cmd_name'
              245  LOAD_FAST                'cmd_hash'
              248  CALL_FUNCTION_3       3  '3 positional, 0 named'
              251  POP_JUMP_IF_FALSE   394  'to 394'

 L. 342       254  SETUP_EXCEPT        322  'to 322'

 L. 343       257  LOAD_FAST                'cmd_name'
              260  LOAD_FAST                'self'
              263  LOAD_ATTR                response
              266  LOAD_STR                 'name'
              269  STORE_SUBSCR     

 L. 344       270  LOAD_FAST                'cmd_obj'
              273  LOAD_ATTR                run
              276  LOAD_FAST                'cmd_hash'
              279  CALL_FUNCTION_1       1  '1 positional, 0 named'
              282  STORE_FAST               'result'

 L. 345       285  LOAD_FAST                'self'
              288  LOAD_ATTR                intf
              291  LOAD_CONST               -1
              294  BINARY_SUBSCR    
              295  LOAD_ATTR                msg
              298  LOAD_FAST                'self'
              301  LOAD_ATTR                response
              304  CALL_FUNCTION_1       1  '1 positional, 0 named'
              307  POP_TOP          

 L. 346       308  LOAD_FAST                'result'
              311  POP_JUMP_IF_FALSE   318  'to 318'

 L. 346       314  LOAD_FAST                'result'
              317  RETURN_END_IF    
              318  POP_BLOCK        
              319  JUMP_ABSOLUTE       407  'to 407'
            322_0  COME_FROM_EXCEPT    254  '254'

 L. 347       322  DUP_TOP          
              323  LOAD_GLOBAL              Mexcept
              326  LOAD_ATTR                DebuggerQuit

 L. 348       329  LOAD_GLOBAL              Mexcept
              332  LOAD_ATTR                DebuggerRestart
              335  LOAD_GLOBAL              SystemExit
              338  BUILD_TUPLE_3         3 
              341  COMPARE_OP               exception-match
              344  POP_JUMP_IF_FALSE   357  'to 357'
              347  POP_TOP          
              348  POP_TOP          
              349  POP_TOP          

 L. 350       350  RAISE_VARARGS_0       0  'reraise'
              353  POP_EXCEPT       
              354  JUMP_ABSOLUTE       407  'to 407'

 L. 351       357  POP_TOP          
              358  POP_TOP          
              359  POP_TOP          

 L. 352       360  LOAD_GLOBAL              Mmsg
              363  LOAD_ATTR                errmsg
              366  LOAD_FAST                'self'
              369  LOAD_STR                 'INTERNAL ERROR: '

 L. 353       372  LOAD_GLOBAL              traceback
              375  LOAD_ATTR                format_exc
              378  CALL_FUNCTION_0       0  '0 positional, 0 named'
              381  BINARY_ADD       
              382  CALL_FUNCTION_2       2  '2 positional, 0 named'
              385  POP_TOP          

 L. 354       386  POP_EXCEPT       
              387  JUMP_ABSOLUTE       407  'to 407'
              390  END_FINALLY      

 L. 355       391  JUMP_ABSOLUTE       410  'to 410'

 L. 357       394  LOAD_FAST                'self'
              397  LOAD_ATTR                undefined_cmd
              400  LOAD_FAST                'cmd_name'
              403  CALL_FUNCTION_1       1  '1 positional, 0 named'
              406  POP_TOP          
            407_0  COME_FROM_EXCEPT_CLAUSE   354  '354'

 L. 359       407  JUMP_FORWARD        410  'to 410'
            410_0  COME_FROM           407  '407'

 L. 360       410  LOAD_CONST               False
              413  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_EXCEPT_CLAUSE' instruction at offset 407_0

    def remove_preloop_hook(self, hook):
        try:
            position = self.preloop_hooks.index(hook)
        except ValueError:
            return False

        del self.preloop_hooks[position]
        return True

    def setup(self):
        """Initialization done before entering the debugger-command
        loop. In particular we set up the call stack used for local
        variable lookup and frame/up/down commands.

        We return True if we should NOT enter the debugger-command
        loop."""
        self.forget()
        if self.settings('dbg_trepan'):
            self.frame = inspect.currentframe()
        if self.event in ('exception', 'c_exception'):
            exc_type, exc_value, exc_traceback = self.event_arg
        else:
            _, _, exc_traceback = (None, None, None)
        if self.frame or exc_traceback:
            self.stack, self.curindex = get_stack(self.frame, exc_traceback, None, self)
            self.curframe = self.stack[self.curindex][0]
            self.thread_name = Mthread.current_thread_name()
        else:
            self.stack = self.curframe = self.botframe = None
        if self.curframe:
            self.list_lineno = max(1, inspect.getlineno(self.curframe))
        else:
            self.list_lineno = None
        return False

    def undefined_cmd(self, cmd):
        """Error message when a command doesn't exist"""
        Mmsg.errmsg(self, 'Undefined command: "%s". Try "help".' % cmd)

    def _populate_commands(self):
        """ Create an instance of each of the debugger
        commands. Commands are found by importing files in the
        directory 'command'. Some files are excluded via an array set
        in __init__.  For each of the remaining files, we import them
        and scan for class names inside those files and for each class
        name, we will create an instance of that class. The set of
        DebuggerCommand class instances form set of possible debugger
        commands."""
        cmd_instances = []
        from trepan.bwprocessor import command as Mcommand
        eval_cmd_template = 'command_mod.%s(self)'
        for mod_name in Mcommand.__modules__:
            import_name = 'command.' + mod_name
            try:
                command_mod = getattr(__import__(import_name), mod_name)
            except:
                print('Error importing %s: %s' % (mod_name, sys.exc_info()[0]))
                continue

            classnames = [tup[0] for tup in inspect.getmembers(command_mod, inspect.isclass) if 'DebuggerCommand' != tup[0] and tup[0].endswith('Command')]
            for classname in classnames:
                eval_cmd = eval_cmd_template % classname
                try:
                    instance = eval(eval_cmd)
                    cmd_instances.append(instance)
                except:
                    print('Error loading %s from %s: %s' % (
                     classname, mod_name, sys.exc_info()[0]))

        return cmd_instances

    def _populate_cmd_lists(self):
        """ Populate self.commands"""
        self.commands = {}
        for cmd_instance in self.cmd_instances:
            cmd_name = cmd_instance.name
            self.commands[cmd_name] = cmd_instance


if __name__ == '__main__':
    from trepan.interfaces import bullwinkle as Mbullwinkle

    class Debugger:

        def __init__(self):
            self.intf = [
             Mbullwinkle.BWInterface()]
            self.settings = {'dbg_trepan': True,  'reload': False}


    class MockCore:

        def filename(self, fn):
            return fn

        def canonic_filename(self, frame):
            return frame.f_code.co_filename

        def __init__(self):
            self.debugger = Debugger()


    core = MockCore()
    bwproc = BWProcessor(core)
    print('commands:')
    commands = list(bwproc.commands.keys())
    commands.sort()
    print(commands)
    print(resolve_name(bwproc, 'quit'))
    bwproc.frame = sys._getframe()
    bwproc.setup()
    Mlocation.print_location(bwproc)