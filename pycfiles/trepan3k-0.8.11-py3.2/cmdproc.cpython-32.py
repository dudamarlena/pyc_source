# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/cmdproc.py
# Compiled at: 2019-09-30 20:52:09
import inspect, linecache, os, sys, shlex, tempfile, traceback, re, pyficache
from trepan.processor import cmdfns
from trepan.lib.deparse import deparse_and_cache
try:
    from reprlib import Repr
except:
    from reprlib import repr as Repr

from pygments.console import colorize
from tracer import EVENT2SHORT
from trepan import vprocessor as Mprocessor
from trepan.lib import bytecode as Mbytecode
from trepan import exception as Mexcept
from trepan.lib import display as Mdisplay
from trepan import misc as Mmisc
from trepan.lib import file as Mfile
from trepan.lib import stack as Mstack
from trepan.lib import thred as Mthread
from trepan.processor import complete as Mcomplete
from trepan.processor.cmdfns import deparse_fn
warned_file_mismatches = set()

def get_srcdir():
    filename = os.path.normcase(os.path.dirname(os.path.abspath(__file__)))
    return os.path.realpath(filename)


def arg_split(s, posix=False):
    """Split a command line's arguments in a shell-like manner returned
    as a list of lists. Use ';;' with white space to indicate separate
    commands.

    This is a modified version of the standard library's shlex.split()
    function, but with a default of posix=False for splitting, so that quotes
    in inputs are respected.
    """
    args_list = [[]]
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    lex = shlex.shlex(s, posix=posix)
    lex.whitespace_split = True
    args = list(lex)
    for arg in args:
        if ';;' == arg:
            args_list.append([])
        else:
            args_list[(-1)].append(arg)

    return args_list


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
    if command_name.lower() not in obj.commands:
        if command_name in obj.aliases:
            command_name = obj.aliases[command_name]
        else:
            return
    try:
        return command_name.lower()
    except:
        return

    return


def print_source_line(msg, lineno, line, event_str=None):
    """Print out a source line of text , e.g. the second
    line in:
        (/tmp.py:2):  <module>
        L -- 2 import sys,os
        (trepan3k)

    We define this method
    specifically so it can be customized for such applications
    like ipython."""
    return msg('%s %d %s' % (event_str, lineno, line))


def print_source_location_info(print_fn, filename, lineno, fn_name=None, f_lasti=None, remapped_file=None):
    """Print out a source location , e.g. the first line in
    line in:
        (/tmp.py:2 @21):  <module>
        L -- 2 import sys,os
        (trepan3k)
    """
    if remapped_file:
        mess = '(%s:%s remapped %s' % (remapped_file, lineno, filename)
    else:
        mess = '(%s:%s' % (filename, lineno)
    if f_lasti and f_lasti != -1:
        mess += ' @%d' % f_lasti
    mess += '):'
    if fn_name and fn_name != '?':
        mess += ' %s' % fn_name
    print_fn(mess)


def print_location(proc_obj):
    """Show where we are. GUI's and front-end interfaces often
    use this to update displays. So it is helpful to make sure
    we give at least some place that's located in a file.
    """
    i_stack = proc_obj.curindex
    if i_stack is None or proc_obj.stack is None:
        return False
    else:
        core_obj = proc_obj.core
        dbgr_obj = proc_obj.debugger
        intf_obj = dbgr_obj.intf[(-1)]
        remapped_file = None
        source_text = None
        while i_stack >= 0:
            frame_lineno = proc_obj.stack[i_stack]
            i_stack -= 1
            frame, lineno = frame_lineno
            filename = Mstack.frame2file(core_obj, frame, canonic=False)
            if '<string>' == filename and dbgr_obj.eval_string:
                remapped_file = filename
                filename = pyficache.unmap_file(filename)
                if '<string>' == filename:
                    remapped = cmdfns.source_tempfile_remap('eval_string', dbgr_obj.eval_string)
                    pyficache.remap_file(filename, remapped)
                    filename, lineno = pyficache.unmap_file_line(filename, lineno)
            else:
                if '<string>' == filename:
                    source_text = deparse_fn(frame.f_code)
                    filename = "<string: '%s'>" % source_text
                else:
                    m = re.search('^<frozen (.*)>', filename)
            if m and m.group(1) in pyficache.file2file_remap:
                remapped_file = pyficache.file2file_remap[m.group(1)]
            else:
                if filename in pyficache.file2file_remap:
                    remapped_file = pyficache.unmap_file(filename)
                    if remapped_file == filename:
                        remapped_file = None
                elif m and m.group(1) in sys.modules:
                    remapped_file = m.group(1)
                    pyficache.remap_file(filename, remapped_file)
                opts = {'reload_on_change': proc_obj.settings('reload'), 
                 'output': proc_obj.settings('highlight')}
                if 'style' in proc_obj.debugger.settings:
                    opts['style'] = proc_obj.settings('style')
                pyficache.update_cache(filename)
                line = pyficache.getline(filename, lineno, opts)
                if not line:
                    if not source_text and filename.startswith('<string: ') and proc_obj.curframe.f_code:
                        co = proc_obj.curframe.f_code
                        temp_filename, name_for_code = deparse_and_cache(co, proc_obj.errmsg)
                        lineno = 1
                        if temp_filename:
                            filename = temp_filename
                    else:
                        if source_text:
                            lines = source_text.split('\n')
                            temp_name = 'string-'
                        else:
                            lines = linecache.getlines(filename)
                            temp_name = filename
                    if lines:
                        prefix = os.path.basename(temp_name).split('.')[0]
                        fd = tempfile.NamedTemporaryFile(suffix='.py', prefix=prefix, delete=False)
                        with fd:
                            fd.write(''.join(lines).encode('utf-8'))
                            remapped_file = fd.name
                            pyficache.remap_file(remapped_file, filename)
                        fd.close()
                    line = linecache.getline(filename, lineno, proc_obj.curframe.f_globals)
                    if not line:
                        m = re.search('^<frozen (.*)>', filename)
                        if m and m.group(1):
                            remapped_file = m.group(1)
                            try_module = sys.modules.get(remapped_file)
                            if try_module and inspect.ismodule(try_module) and hasattr(try_module, '__file__'):
                                remapped_file = sys.modules[remapped_file].__file__
                                pyficache.remap_file(filename, remapped_file)
                                line = linecache.getline(remapped_file, lineno, proc_obj.curframe.f_globals)
                            else:
                                remapped_file = m.group(1)
                            code = proc_obj.curframe.f_code
                            filename, line = cmdfns.deparse_getline(code, remapped_file, lineno, opts)
                try:
                    match, reason = Mstack.check_path_with_frame(frame, filename)
                    if not match:
                        if filename not in warned_file_mismatches:
                            proc_obj.errmsg(reason)
                            warned_file_mismatches.add(filename)
                except:
                    pass

                fn_name = frame.f_code.co_name
                last_i = frame.f_lasti
                print_source_location_info(intf_obj.msg, filename, lineno, fn_name, remapped_file=remapped_file, f_lasti=last_i)
                if line and len(line.strip()) != 0:
                    if proc_obj.event:
                        print_source_line(intf_obj.msg, lineno, line, proc_obj.event2short[proc_obj.event])
            if '<string>' != filename:
                break

        if proc_obj.event in ('return', 'exception'):
            val = proc_obj.event_arg
            intf_obj.msg('R=> %s' % proc_obj._saferepr(val))
        return True


DEFAULT_PROC_OPTS = {'initfile_list': []}

class CommandProcessor(Mprocessor.Processor):

    def __init__(self, core_obj, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, DEFAULT_PROC_OPTS)
        Mprocessor.Processor.__init__(self, core_obj)
        self.continue_running = False
        self.event2short = dict(EVENT2SHORT)
        self.event2short['signal'] = '?!'
        self.event2short['brkpt'] = 'xx'
        self.optional_modules = ('ipython', 'bpy')
        self.cmd_instances = self._populate_commands()
        self.cmd_argstr = ''
        self.cmd_name = ''
        self.cmd_queue = []
        self.completer = lambda text, state: Mcomplete.completer(self, text, state)
        self.current_command = ''
        self.debug_nest = 1
        self.display_mgr = Mdisplay.DisplayMgr()
        self.intf = core_obj.debugger.intf
        self.last_command = None
        self.precmd_hooks = []
        self.location = lambda : print_location(self)
        self.preloop_hooks = []
        self.postcmd_hooks = []
        self._populate_cmd_lists()
        self.prompt_str = '(trepan3k) '
        self.different_line = None
        self.curframe = None
        self.event = None
        self.event_arg = None
        self.frame = None
        self.list_lineno = 0
        self.list_offset = -1
        self.list_obj = None
        self.list_filename = None
        self.list_orig_lineno = 0
        self.list_filename = None
        self.macros = {}
        self._repr = Repr()
        self._repr.maxstring = 100
        self._repr.maxother = 60
        self._repr.maxset = 10
        self._repr.maxfrozen = 10
        self._repr.array = 10
        self.stack = []
        self.thread_name = None
        self.frame_thread_name = None
        initfile_list = get_option('initfile_list')
        for init_cmdfile in initfile_list:
            self.queue_startfile(init_cmdfile)

        return

    def _saferepr(self, str, maxwidth=None):
        if maxwidth is None:
            maxwidth = self.debugger.settings['width']
        return self._repr.repr(str)[:maxwidth]

    def add_preloop_hook(self, hook, position=-1, nodups=True):
        if hook in self.preloop_hooks:
            return False
        self.preloop_hooks.insert(position, hook)
        return True

    def defaultFile(self):
        """Produce a reasonable default."""
        filename = self.curframe.f_code.co_filename
        if filename == '<string>' and self.debugger.mainpyfile:
            filename = self.debugger.mainpyfile
        return filename

    def set_prompt(self, prompt='trepan3k'):
        if self.thread_name and self.thread_name != 'MainThread':
            prompt += ':' + self.thread_name
        self.prompt_str = '%s%s%s' % ('(' * self.debug_nest,
         prompt,
         ')' * self.debug_nest)
        highlight = self.debugger.settings['highlight']
        if highlight and highlight in ('light', 'dark'):
            self.prompt_str = colorize('underline', self.prompt_str)
        self.prompt_str += ' '

    def event_processor(self, frame, event, event_arg, prompt='trepan3k'):
        """command event processor: reading a commands do something with them."""
        self.frame = frame
        self.event = event
        self.event_arg = event_arg
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        line = linecache.getline(filename, lineno, frame.f_globals)
        if not line:
            opts = {'output': 'plain',  'reload_on_change': self.settings('reload'),  'strip_nl': False}
            m = re.search('^<frozen (.*)>', filename)
            if m and m.group(1):
                filename = pyficache.unmap_file(m.group(1))
            line = pyficache.getline(filename, lineno, opts)
        self.current_source_text = line
        if self.settings('skip') is not None:
            if Mbytecode.is_def_stmt(line, frame):
                return True
            if Mbytecode.is_class_def(line, frame):
                return True
        self.thread_name = Mthread.current_thread_name()
        self.frame_thread_name = self.thread_name
        self.set_prompt(prompt)
        self.process_commands()
        if filename == '<string>':
            pyficache.remove_remap_file('<string>')
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
            self.errmsg(str('%s: %s' % (exc_type_name, arg)))
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
            if type(t) == bytes:
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            self.errmsg('%s: %s' % (str(exc_type_name), str(v)))

        return

    def get_an_int(self, arg, msg_on_error, min_value=None, max_value=None):
        """Like cmdfns.get_an_int(), but if there's a stack frame use that
        in evaluation."""
        ret_value = self.get_int_noerr(arg)
        if ret_value is None:
            if msg_on_error:
                self.errmsg(msg_on_error)
            else:
                self.errmsg('Expecting an integer, got: %s.' % str(arg))
            return
        else:
            if min_value and ret_value < min_value:
                self.errmsg('Expecting integer value to be at least %d, got: %d.' % (
                 min_value, ret_value))
                return
            if max_value and ret_value > max_value:
                self.errmsg('Expecting integer value to be at most %d, got: %d.' % (
                 max_value, ret_value))
                return
            return ret_value

    def get_int_noerr(self, arg):
        """Eval arg and it is an integer return the value. Otherwise
        return None"""
        if self.curframe:
            g = self.curframe.f_globals
            l = self.curframe.f_locals
        else:
            g = globals()
            l = locals()
        try:
            val = int(eval(arg, g, l))
        except (SyntaxError, NameError, ValueError, TypeError):
            return

        return val

    def get_int(self, arg, min_value=0, default=1, cmdname=None, at_most=None):
        """If no argument use the default. If arg is a an integer between
        least min_value and at_most, use that. Otherwise report an error.
        If there's a stack frame use that in evaluation."""
        if arg is None:
            return default
        else:
            default = self.get_int_noerr(arg)
            if default is None:
                if cmdname:
                    self.errmsg(("Command '%s' expects an integer; " + 'got: %s.') % (cmdname, str(arg)))
                else:
                    self.errmsg('Expecting a positive integer, got: %s' % str(arg))
                return
            else:
                if default < min_value:
                    if cmdname:
                        self.errmsg(("Command '%s' expects an integer at least" + ' %d; got: %d.') % (
                         cmdname, min_value, default))
                else:
                    self.errmsg(('Expecting a positive integer at least' + ' %d; got: %d') % (
                     min_value, default))
                return
            if at_most and default > at_most:
                if cmdname:
                    self.errmsg(("Command '%s' expects an integer at most" + ' %d; got: %d.') % (
                     cmdname, at_most, default))
                else:
                    self.errmsg('Expecting an integer at most %d; got: %d' % (
                     at_most, default))
            return default

    def getval(self, arg, locals=None):
        if not locals:
            locals = self.curframe.f_locals
        try:
            return eval(arg, self.curframe.f_globals, locals)
        except:
            t, v = sys.exc_info()[:2]
            if isinstance(t, str):
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            self.errmsg(str('%s: %s' % (exc_type_name, arg)))
            raise

    def ok_for_running(self, cmd_obj, name, nargs):
        """We separate some of the common debugger command checks here:
        whether it makes sense to run the command in this execution state,
        if the command has the right number of arguments and so on.
        """
        if hasattr(cmd_obj, 'execution_set'):
            if self.core.execution_status not in cmd_obj.execution_set:
                part1 = "Command '%s' is not available for execution status:" % name
                mess = Mmisc.wrapped_lines(part1, self.core.execution_status, self.debugger.settings['width'])
                self.errmsg(mess)
                return False
        if self.frame is None and cmd_obj.need_stack:
            self.intf[(-1)].errmsg("Command '%s' needs an execution stack." % name)
            return False
        else:
            if nargs < cmd_obj.min_args:
                self.errmsg(("Command '%s' needs at least %d argument(s); " + 'got %d.') % (
                 name, cmd_obj.min_args, nargs))
                return False
            if cmd_obj.max_args is not None and nargs > cmd_obj.max_args:
                self.errmsg(("Command '%s' can take at most %d argument(s);" + ' got %d.') % (
                 name, cmd_obj.max_args, nargs))
                return False
            return True

    def process_commands(self):
        """Handle debugger commands."""
        if self.core.execution_status != 'No program':
            self.setup()
            self.location()
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

 L. 677         0  LOAD_GLOBAL              len
                3  LOAD_FAST                'self'
                6  LOAD_ATTR                cmd_queue
                9  CALL_FUNCTION_1       1  '1 positional, 0 named'
               12  LOAD_CONST               0
               15  COMPARE_OP               >
               18  POP_JUMP_IF_FALSE    53  'to 53'

 L. 678        21  LOAD_FAST                'self'
               24  LOAD_ATTR                cmd_queue
               27  LOAD_CONST               0
               30  BINARY_SUBSCR    
               31  LOAD_ATTR                strip
               34  CALL_FUNCTION_0       0  '0 positional, 0 named'
               37  STORE_FAST               'current_command'

 L. 679        40  LOAD_FAST                'self'
               43  LOAD_ATTR                cmd_queue
               46  LOAD_CONST               0
               49  DELETE_SUBSCR    
               50  JUMP_FORWARD        124  'to 124'
               53  ELSE                     '124'

 L. 682        53  LOAD_FAST                'self'
               56  LOAD_ATTR                intf
               59  LOAD_CONST               -1
               62  BINARY_SUBSCR    
               63  LOAD_ATTR                read_command
               66  LOAD_FAST                'self'
               69  LOAD_ATTR                prompt_str
               72  CALL_FUNCTION_1       1  '1 positional, 0 named'
               75  LOAD_ATTR                strip
               78  CALL_FUNCTION_0       0  '0 positional, 0 named'
               81  STORE_FAST               'current_command'

 L. 683        84  LOAD_STR                 ''
               87  LOAD_FAST                'current_command'
               90  COMPARE_OP               ==
               93  POP_JUMP_IF_FALSE   124  'to 124'
               96  LOAD_FAST                'self'
               99  LOAD_ATTR                intf
              102  LOAD_CONST               -1
              105  BINARY_SUBSCR    
              106  LOAD_ATTR                interactive
            109_0  COME_FROM            93  '93'
              109  POP_JUMP_IF_FALSE   124  'to 124'

 L. 684       112  LOAD_FAST                'self'
              115  LOAD_ATTR                last_command
              118  STORE_FAST               'current_command'

 L. 685       121  JUMP_FORWARD        124  'to 124'
            124_0  COME_FROM           121  '121'
            124_1  COME_FROM            50  '50'

 L. 688       124  LOAD_STR                 ''
              127  LOAD_FAST                'current_command'
              130  COMPARE_OP               ==
              133  POP_JUMP_IF_FALSE   176  'to 176'

 L. 689       136  LOAD_FAST                'self'
              139  LOAD_ATTR                intf
              142  LOAD_CONST               -1
              145  BINARY_SUBSCR    
              146  LOAD_ATTR                interactive
              149  POP_JUMP_IF_FALSE   172  'to 172'

 L. 690       152  LOAD_FAST                'self'
              155  LOAD_ATTR                errmsg
              158  LOAD_STR                 'No previous command registered, '

 L. 691       161  LOAD_STR                 'so this is a no-op.'
              164  BINARY_ADD       
              165  CALL_FUNCTION_1       1  '1 positional, 0 named'
              168  POP_TOP          

 L. 692       169  JUMP_FORWARD        172  'to 172'
            172_0  COME_FROM           169  '169'

 L. 693       172  LOAD_CONST               False
              175  RETURN_END_IF    

 L. 694       176  LOAD_FAST                'current_command'
              179  LOAD_CONST               None
              182  COMPARE_OP               is
              185  POP_JUMP_IF_TRUE    204  'to 204'
              188  LOAD_FAST                'current_command'
              191  LOAD_CONST               0
              194  BINARY_SUBSCR    
              195  LOAD_STR                 '#'
              198  COMPARE_OP               ==
            201_0  COME_FROM           185  '185'
              201  POP_JUMP_IF_FALSE   208  'to 208'

 L. 695       204  LOAD_CONST               False
              207  RETURN_END_IF    

 L. 696       208  SETUP_EXCEPT        227  'to 227'

 L. 697       211  LOAD_GLOBAL              arg_split
              214  LOAD_FAST                'current_command'
              217  CALL_FUNCTION_1       1  '1 positional, 0 named'
              220  STORE_FAST               'args_list'
              223  POP_BLOCK        
              224  JUMP_FORWARD        272  'to 272'
            227_0  COME_FROM_EXCEPT    208  '208'

 L. 698       227  POP_TOP          
              228  POP_TOP          
              229  POP_TOP          

 L. 699       230  LOAD_FAST                'self'
              233  LOAD_ATTR                errmsg
              236  LOAD_STR                 'bad parse %s: %s'
              239  LOAD_GLOBAL              sys
              242  LOAD_ATTR                exc_info
              245  CALL_FUNCTION_0       0  '0 positional, 0 named'
              248  LOAD_CONST               0
              251  LOAD_CONST               2
              254  BUILD_SLICE_2         2 
              257  BINARY_SUBSCR    
              258  BINARY_MODULO    
              259  CALL_FUNCTION_1       1  '1 positional, 0 named'
              262  POP_TOP          

 L. 700       263  LOAD_CONST               False
              266  RETURN_VALUE     
              267  POP_EXCEPT       
              268  JUMP_FORWARD        272  'to 272'
              271  END_FINALLY      
            272_0  COME_FROM           268  '268'
            272_1  COME_FROM           224  '224'

 L. 702       272  SETUP_LOOP         1010  'to 1010'
              275  LOAD_FAST                'args_list'
              278  GET_ITER         
              279  FOR_ITER           1009  'to 1009'
              282  STORE_FAST               'args'

 L. 703       285  LOAD_GLOBAL              len
              288  LOAD_FAST                'args'
              291  CALL_FUNCTION_1       1  '1 positional, 0 named'
              294  POP_JUMP_IF_FALSE   279  'to 279'

 L. 704       297  SETUP_LOOP          722  'to 722'

 L. 705       300  LOAD_GLOBAL              len
              303  LOAD_FAST                'args'
              306  CALL_FUNCTION_1       1  '1 positional, 0 named'
              309  LOAD_CONST               0
              312  COMPARE_OP               ==
              315  POP_JUMP_IF_FALSE   322  'to 322'

 L. 705       318  LOAD_CONST               False
              321  RETURN_END_IF    

 L. 706       322  LOAD_FAST                'args'
              325  LOAD_CONST               0
              328  BINARY_SUBSCR    
              329  STORE_FAST               'macro_cmd_name'

 L. 707       332  LOAD_FAST                'macro_cmd_name'
              335  LOAD_FAST                'self'
              338  LOAD_ATTR                macros
              341  COMPARE_OP               not-in
              344  POP_JUMP_IF_FALSE   351  'to 351'

 L. 707       347  BREAK_LOOP       
              348  JUMP_FORWARD        351  'to 351'
            351_0  COME_FROM           348  '348'

 L. 708       351  SETUP_EXCEPT        391  'to 391'

 L. 710       354  LOAD_FAST                'self'
              357  LOAD_ATTR                macros
              360  LOAD_FAST                'macro_cmd_name'
              363  BINARY_SUBSCR    
              364  LOAD_CONST               0
              367  BINARY_SUBSCR    
              368  LOAD_FAST                'args'
              371  LOAD_CONST               1
              374  LOAD_CONST               None
              377  BUILD_SLICE_2         2 
              380  BINARY_SUBSCR    
              381  CALL_FUNCTION_VAR_0     0  '0 positional, 0 named'
              384  STORE_FAST               'current_command'
              387  POP_BLOCK        
              388  JUMP_FORWARD        458  'to 458'
            391_0  COME_FROM_EXCEPT    351  '351'

 L. 711       391  DUP_TOP          
              392  LOAD_GLOBAL              TypeError
              395  COMPARE_OP               exception-match
              398  POP_JUMP_IF_FALSE   457  'to 457'
              401  POP_TOP          
              402  POP_TOP          
              403  POP_TOP          

 L. 712       404  LOAD_GLOBAL              sys
              407  LOAD_ATTR                exc_info
              410  CALL_FUNCTION_0       0  '0 positional, 0 named'
              413  LOAD_CONST               None
              416  LOAD_CONST               2
              419  BUILD_SLICE_2         2 
              422  BINARY_SUBSCR    
              423  UNPACK_SEQUENCE_2     2 
              426  STORE_FAST               't'
              429  STORE_FAST               'v'

 L. 713       432  LOAD_FAST                'self'
              435  LOAD_ATTR                errmsg
              438  LOAD_STR                 'Error expanding macro %s'

 L. 714       441  LOAD_FAST                'macro_cmd_name'
              444  BINARY_MODULO    
              445  CALL_FUNCTION_1       1  '1 positional, 0 named'
              448  POP_TOP          

 L. 715       449  LOAD_CONST               False
              452  RETURN_VALUE     
              453  POP_EXCEPT       
              454  JUMP_FORWARD        458  'to 458'
              457  END_FINALLY      
            458_0  COME_FROM           454  '454'
            458_1  COME_FROM           388  '388'

 L. 716       458  LOAD_FAST                'self'
              461  LOAD_ATTR                settings
              464  LOAD_STR                 'debugmacro'
              467  CALL_FUNCTION_1       1  '1 positional, 0 named'
              470  POP_JUMP_IF_FALSE   486  'to 486'

 L. 717       473  LOAD_GLOBAL              print
              476  LOAD_FAST                'current_command'
              479  CALL_FUNCTION_1       1  '1 positional, 0 named'
              482  POP_TOP          

 L. 718       483  JUMP_FORWARD        486  'to 486'
            486_0  COME_FROM           483  '483'

 L. 719       486  LOAD_GLOBAL              isinstance
              489  LOAD_GLOBAL              types
              492  LOAD_ATTR                ListType
              495  LOAD_GLOBAL              type
              498  LOAD_FAST                'current_command'
              501  CALL_FUNCTION_1       1  '1 positional, 0 named'
              504  CALL_FUNCTION_2       2  '2 positional, 0 named'
              507  POP_JUMP_IF_FALSE   649  'to 649'

 L. 720       510  SETUP_LOOP          594  'to 594'
              513  LOAD_FAST                'current_command'
              516  GET_ITER         
              517  FOR_ITER            593  'to 593'
              520  STORE_FAST               'x'

 L. 721       523  LOAD_GLOBAL              str
              526  LOAD_GLOBAL              type
              529  LOAD_FAST                'x'
              532  CALL_FUNCTION_1       1  '1 positional, 0 named'
              535  COMPARE_OP               !=
              538  POP_JUMP_IF_FALSE   517  'to 517'

 L. 722       541  LOAD_FAST                'self'
              544  LOAD_ATTR                errmsg
              547  LOAD_STR                 'macro %s should return a List '

 L. 723       550  LOAD_STR                 'of Strings. Has %s of type %s'
              553  BINARY_ADD       

 L. 724       554  LOAD_FAST                'macro_cmd_name'
              557  LOAD_FAST                'x'

 L. 725       560  LOAD_GLOBAL              repr
              563  LOAD_FAST                'current_command'
              566  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 726       569  LOAD_GLOBAL              type
              572  LOAD_FAST                'x'
              575  CALL_FUNCTION_1       1  '1 positional, 0 named'
              578  BUILD_TUPLE_4         4 
              581  BINARY_MODULO    
              582  CALL_FUNCTION_1       1  '1 positional, 0 named'
              585  POP_TOP          

 L. 727       586  LOAD_CONST               False
              589  RETURN_END_IF    

 L. 728       590  JUMP_BACK           517  'to 517'
              593  POP_BLOCK        
            594_0  COME_FROM_LOOP      510  '510'

 L. 730       594  LOAD_FAST                'current_command'
              597  LOAD_CONST               0
              600  BINARY_SUBSCR    
              601  STORE_FAST               'first'

 L. 731       604  LOAD_FAST                'first'
              607  LOAD_ATTR                split
              610  CALL_FUNCTION_0       0  '0 positional, 0 named'
              613  STORE_FAST               'args'

 L. 732       616  LOAD_FAST                'self'
              619  LOAD_ATTR                cmd_queue
              622  LOAD_FAST                'current_command'
              625  LOAD_CONST               1
              628  LOAD_CONST               None
              631  BUILD_SLICE_2         2 
              634  BINARY_SUBSCR    
              635  BUILD_LIST_1          1 
              638  BINARY_ADD       
              639  POP_TOP          

 L. 733       640  LOAD_FAST                'first'
              643  STORE_FAST               'current_command'
              646  JUMP_BACK           300  'to 300'

 L. 734       649  LOAD_GLOBAL              type
              652  LOAD_FAST                'current_command'
              655  CALL_FUNCTION_1       1  '1 positional, 0 named'
              658  LOAD_GLOBAL              str
              661  COMPARE_OP               ==
              664  POP_JUMP_IF_FALSE   682  'to 682'

 L. 735       667  LOAD_FAST                'current_command'
              670  LOAD_ATTR                split
              673  CALL_FUNCTION_0       0  '0 positional, 0 named'
              676  STORE_FAST               'args'
              679  JUMP_BACK           300  'to 300'

 L. 737       682  LOAD_FAST                'self'
              685  LOAD_ATTR                errmsg
              688  LOAD_STR                 'macro %s should return a List '

 L. 738       691  LOAD_STR                 'of Strings or a String. Got %s'
              694  BINARY_ADD       

 L. 739       695  LOAD_FAST                'macro_cmd_name'
              698  LOAD_GLOBAL              repr
              701  LOAD_FAST                'current_command'
              704  CALL_FUNCTION_1       1  '1 positional, 0 named'
              707  BUILD_TUPLE_2         2 
              710  BINARY_MODULO    
              711  CALL_FUNCTION_1       1  '1 positional, 0 named'
              714  POP_TOP          

 L. 740       715  LOAD_CONST               False
              718  RETURN_VALUE     

 L. 741       719  CONTINUE            300  'to 300'
            722_0  COME_FROM_LOOP      297  '297'

 L. 743       722  LOAD_FAST                'args'
              725  LOAD_CONST               0
              728  BINARY_SUBSCR    
              729  LOAD_FAST                'self'
              732  STORE_ATTR               cmd_name

 L. 744       735  LOAD_GLOBAL              resolve_name
              738  LOAD_FAST                'self'
              741  LOAD_FAST                'self'
              744  LOAD_ATTR                cmd_name
              747  CALL_FUNCTION_2       2  '2 positional, 0 named'
              750  STORE_FAST               'cmd_name'

 L. 745       753  LOAD_FAST                'current_command'
              756  LOAD_GLOBAL              len
              759  LOAD_FAST                'self'
              762  LOAD_ATTR                cmd_name
              765  CALL_FUNCTION_1       1  '1 positional, 0 named'
              768  LOAD_CONST               None
              771  BUILD_SLICE_2         2 
              774  BINARY_SUBSCR    
              775  LOAD_ATTR                lstrip
              778  CALL_FUNCTION_0       0  '0 positional, 0 named'
              781  LOAD_FAST                'self'
              784  STORE_ATTR               cmd_argstr

 L. 746       787  LOAD_FAST                'cmd_name'
              790  POP_JUMP_IF_FALSE   959  'to 959'

 L. 747       793  LOAD_FAST                'current_command'
              796  LOAD_FAST                'self'
              799  STORE_ATTR               last_command

 L. 748       802  LOAD_FAST                'self'
              805  LOAD_ATTR                commands
              808  LOAD_FAST                'cmd_name'
              811  BINARY_SUBSCR    
              812  STORE_FAST               'cmd_obj'

 L. 749       815  LOAD_FAST                'self'
              818  LOAD_ATTR                ok_for_running
              821  LOAD_FAST                'cmd_obj'
              824  LOAD_FAST                'cmd_name'
              827  LOAD_GLOBAL              len
              830  LOAD_FAST                'args'
              833  CALL_FUNCTION_1       1  '1 positional, 0 named'
              836  LOAD_CONST               1
              839  BINARY_SUBTRACT  
              840  CALL_FUNCTION_3       3  '3 positional, 0 named'
              843  POP_JUMP_IF_FALSE  1003  'to 1003'

 L. 750       846  SETUP_EXCEPT        887  'to 887'

 L. 751       849  LOAD_FAST                'current_command'
              852  LOAD_FAST                'self'
              855  STORE_ATTR               current_command

 L. 752       858  LOAD_FAST                'cmd_obj'
              861  LOAD_ATTR                run
              864  LOAD_FAST                'args'
              867  CALL_FUNCTION_1       1  '1 positional, 0 named'
              870  STORE_FAST               'result'

 L. 753       873  LOAD_FAST                'result'
              876  POP_JUMP_IF_FALSE   883  'to 883'

 L. 753       879  LOAD_FAST                'result'
              882  RETURN_END_IF    
              883  POP_BLOCK        
              884  JUMP_ABSOLUTE       956  'to 956'
            887_0  COME_FROM_EXCEPT    846  '846'

 L. 754       887  DUP_TOP          
              888  LOAD_GLOBAL              Mexcept
              891  LOAD_ATTR                DebuggerQuit

 L. 755       894  LOAD_GLOBAL              Mexcept
              897  LOAD_ATTR                DebuggerRestart
              900  LOAD_GLOBAL              SystemExit
              903  BUILD_TUPLE_3         3 
              906  COMPARE_OP               exception-match
              909  POP_JUMP_IF_FALSE   922  'to 922'
              912  POP_TOP          
              913  POP_TOP          
              914  POP_TOP          

 L. 757       915  RAISE_VARARGS_0       0  'reraise'
              918  POP_EXCEPT       
              919  JUMP_ABSOLUTE       956  'to 956'

 L. 758       922  POP_TOP          
              923  POP_TOP          
              924  POP_TOP          

 L. 759       925  LOAD_FAST                'self'
              928  LOAD_ATTR                errmsg
              931  LOAD_STR                 'INTERNAL ERROR: '

 L. 760       934  LOAD_GLOBAL              traceback
              937  LOAD_ATTR                format_exc
              940  CALL_FUNCTION_0       0  '0 positional, 0 named'
              943  BINARY_ADD       
              944  CALL_FUNCTION_1       1  '1 positional, 0 named'
              947  POP_TOP          

 L. 761       948  POP_EXCEPT       
              949  JUMP_ABSOLUTE       956  'to 956'
              952  END_FINALLY      

 L. 762       953  JUMP_ABSOLUTE      1003  'to 1003'
            956_0  COME_FROM_EXCEPT_CLAUSE   919  '919'

 L. 763       956  JUMP_ABSOLUTE      1006  'to 1006'
              959  ELSE                     '1003'

 L. 764       959  LOAD_FAST                'self'
              962  LOAD_ATTR                settings
              965  LOAD_STR                 'autoeval'
              968  CALL_FUNCTION_1       1  '1 positional, 0 named'
              971  POP_JUMP_IF_TRUE    990  'to 990'

 L. 765       974  LOAD_FAST                'self'
              977  LOAD_ATTR                undefined_cmd
              980  LOAD_FAST                'current_command'
              983  CALL_FUNCTION_1       1  '1 positional, 0 named'
              986  POP_TOP          
              987  JUMP_ABSOLUTE      1006  'to 1006'
              990  ELSE                     '1003'

 L. 767       990  LOAD_FAST                'self'
              993  LOAD_ATTR                exec_line
              996  LOAD_FAST                'current_command'
              999  CALL_FUNCTION_1       1  '1 positional, 0 named'
             1002  POP_TOP          

 L. 769      1003  CONTINUE            279  'to 279'

 L. 770      1006  JUMP_BACK           279  'to 279'
             1009  POP_BLOCK        
           1010_0  COME_FROM_LOOP      272  '272'

 L. 771      1010  LOAD_CONST               False
             1013  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 722

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
            if exc_traceback:
                self.list_lineno = traceback.extract_tb(exc_traceback, 1)[0][1]
                self.list_offset = self.curframe.f_lasti
                self.list_object = self.curframe
        else:
            self.stack = self.curframe = self.botframe = None
        if self.curframe:
            self.list_lineno = max(1, inspect.getlineno(self.curframe) - int(self.settings('listsize') / 2)) - 1
            self.list_offset = self.curframe.f_lasti
            self.list_filename = self.curframe.f_code.co_filename
            self.list_object = self.curframe
        elif not exc_traceback:
            self.list_lineno = None
        return False

    def queue_startfile(self, cmdfile):
        """Arrange for file of debugger commands to get read in the
        process-command loop."""
        expanded_cmdfile = os.path.expanduser(cmdfile)
        is_readable = Mfile.readable(expanded_cmdfile)
        if is_readable:
            self.cmd_queue.append('source ' + expanded_cmdfile)
        else:
            if is_readable is None:
                self.errmsg("source file '%s' doesn't exist" % expanded_cmdfile)
            else:
                self.errmsg("source file '%s' is not readable" % expanded_cmdfile)
        return

    def undefined_cmd(self, cmd):
        """Error message when a command doesn't exist"""
        self.errmsg('Undefined command: "%s". Try "help".' % cmd)

    def read_history_file(self):
        """Read the command history file -- possibly."""
        histfile = self.debugger.intf[(-1)].histfile
        try:
            import readline
            readline.read_history_file(histfile)
        except IOError:
            pass
        except ImportError:
            pass

    def write_history_file(self):
        """Write the command history file -- possibly."""
        settings = self.debugger.settings
        histfile = self.debugger.intf[(-1)].histfile
        if settings['hist_save']:
            try:
                import readline
                try:
                    readline.write_history_file(histfile)
                except IOError:
                    pass

            except ImportError:
                pass

    def _populate_commands(self):
        """ Create an instance of each of the debugger
        commands. Commands are found by importing files in the
        directory 'command'. Some files are excluded via an array set
        in __init__.  For each of the remaining files, we import them
        and scan for class names inside those files and for each class
        name, we will create an instance of that class. The set of
        DebuggerCommand class instances form set of possible debugger
        commands."""
        from trepan.processor import command as Mcommand
        if hasattr(Mcommand, '__modules__'):
            return self.populate_commands_easy_install(Mcommand)
        else:
            return self.populate_commands_pip(Mcommand)

    def populate_commands_pip(self, Mcommand):
        cmd_instances = []
        eval_cmd_template = 'command_mod.%s(self)'
        for mod_name in Mcommand.__dict__.keys():
            if mod_name.startswith('__'):
                continue
            import_name = 'trepan.processor.command.' + mod_name
            imp = __import__(import_name)
            if imp.__name__ == 'trepan':
                command_mod = imp.processor.command
            else:
                if mod_name in ('info_sub', 'set_sub', 'show_sub'):
                    pass
                try:
                    command_mod = getattr(__import__(import_name), mod_name)
                except:
                    if mod_name not in self.optional_modules:
                        print('Error importing %s: %s' % (
                         mod_name, sys.exc_info()[0]))
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

    def populate_commands_easy_install(self, Mcommand):
        cmd_instances = []
        srcdir = get_srcdir()
        sys.path.insert(0, srcdir)
        for mod_name in Mcommand.__modules__:
            if mod_name in ('info_sub', 'set_sub', 'show_sub'):
                pass
            import_name = 'command.' + mod_name
            try:
                command_mod = getattr(__import__(import_name), mod_name)
            except:
                if mod_name not in self.optional_modules:
                    print('Error importing %s: %s' % (
                     mod_name, sys.exc_info()[0]))
                continue

            classnames = [tup[0] for tup in inspect.getmembers(command_mod, inspect.isclass) if 'DebuggerCommand' != tup[0] and tup[0].endswith('Command')]
            for classname in classnames:
                try:
                    instance = getattr(command_mod, classname)(self)
                    cmd_instances.append(instance)
                except:
                    print('Error loading %s from %s: %s' % (
                     classname, mod_name, sys.exc_info()[0]))

        return cmd_instances

    def _populate_cmd_lists(self):
        """ Populate self.lists and hashes:
        self.commands, and self.aliases, self.category """
        self.commands = {}
        self.aliases = {}
        self.category = {}
        for cmd_instance in self.cmd_instances:
            if not hasattr(cmd_instance, 'aliases'):
                continue
            alias_names = cmd_instance.aliases
            cmd_name = cmd_instance.name
            self.commands[cmd_name] = cmd_instance
            for alias_name in alias_names:
                self.aliases[alias_name] = cmd_name

            cat = getattr(cmd_instance, 'category')
            if cat and self.category.get(cat):
                self.category[cat].append(cmd_name)
            else:
                self.category[cat] = [
                 cmd_name]

        for k in list(self.category.keys()):
            self.category[k].sort()


if __name__ == '__main__':
    from trepan.processor.command import mock as Mmock
    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    print('commands:')
    commands = list(cmdproc.commands.keys())
    commands.sort()
    print(commands)
    print('aliases:')
    aliases = list(cmdproc.aliases.keys())
    aliases.sort()
    print(aliases)
    print(resolve_name(cmdproc, 'quit'))
    print(resolve_name(cmdproc, 'q'))
    print(resolve_name(cmdproc, 'info'))
    print(resolve_name(cmdproc, 'i'))
    cmdproc.frame = sys._getframe()
    cmdproc.setup()
    print()
    print('-' * 10)
    cmdproc.location()
    print('-' * 10)
    print(cmdproc.eval('1+2'))
    print(cmdproc.eval('len(aliases)'))
    import pprint
    print(pprint.pformat(cmdproc.category))
    print(arg_split('Now is the time'))
    print(arg_split('Now is the time ;;'))
    print(arg_split("Now is 'the time'"))
    print(arg_split('Now is the time ;; for all good men'))
    print(arg_split("Now is the time ';;' for all good men"))
    print(cmdproc.commands)
    fn = cmdproc.commands['quit']
    print('Removing non-existing quit hook: %s' % cmdproc.remove_preloop_hook(fn))
    cmdproc.add_preloop_hook(fn)
    print(cmdproc.preloop_hooks)
    print('Removed existing quit hook: %s' % cmdproc.remove_preloop_hook(fn))