# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/cmdproc.py
# Compiled at: 2013-03-24 09:41:43
import inspect, linecache, os, sys, shlex, tempfile, traceback, types, pyficache
from repr import Repr
from import_relative import import_relative, get_srcdir
from tracer import EVENT2SHORT
Mprocessor = import_relative('vprocessor', '..', 'pydbgr')
Mbytecode = import_relative('bytecode', '..lib', 'pydbgr')
Mexcept = import_relative('exception', '..', 'pydbgr')
Mdisplay = import_relative('display', '..lib', 'pydbgr')
Mmisc = import_relative('misc', '..', 'pydbgr')
Mfile = import_relative('file', '..lib', 'pydbgr')
Mstack = import_relative('stack', '..lib', 'pydbgr')
Mthread = import_relative('thread', '..lib', 'pydbgr')

def arg_split(s, posix=False):
    """Split a command line's arguments in a shell-like manner returned
    as a list of lists. Use ';;' with white space to indicate separate
    commands.

    This is a modified version of the standard library's shlex.split()
    function, but with a default of posix=False for splitting, so that quotes
    in inputs are respected.
    """
    args_list = [[]]
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
        dbg = proc_obj.debugger
        settings = proc_obj.debugger.settings
        if not settings['dbg_pydbgr']:
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

    return (
     stack, i)


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
        (Pydbgr)

    We define this method
    specifically so it can be customized for such applications
    like ipython."""
    return msg('%s %d %s' % (event_str, lineno, line))


def print_source_location_info(print_fn, filename, lineno, fn_name=None, f_lasti=None, remapped_file=None):
    """Print out a source location , e.g. the first line in
    line in:
        (/tmp.py:2):  <module>
        L -- 2 import sys,os
        (Pydbgr)
    """
    mess = '(%s:%s' % (filename, lineno)
    if remapped_file:
        mess += ' remapped %s' % remapped_file
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
    core_obj = proc_obj.core
    dbgr_obj = proc_obj.debugger
    intf_obj = dbgr_obj.intf[(-1)]
    remapped_file = None
    while i_stack >= 0:
        frame_lineno = proc_obj.stack[i_stack]
        i_stack -= 1
        (frame, lineno) = frame_lineno
        filename = Mstack.frame2file(core_obj, frame)
        if '<string>' == filename and dbgr_obj.eval_string:
            remapped_file = filename
            filename = pyficache.unmap_file(filename)
            if '<string>' == filename:
                fd = tempfile.NamedTemporaryFile(suffix='.py', prefix='eval_string', delete=False)
                fd.write(dbgr_obj.eval_string)
                fd.close()
                pyficache.remap_file(fd.name, '<string>')
                filename = fd.name
        fn_name = frame.f_code.co_name
        print_source_location_info(intf_obj.msg, filename, lineno, fn_name, remapped_file=remapped_file)
        opts = {'reload_on_change': proc_obj.settings('reload'), 'output': proc_obj.settings('highlight')}
        line = pyficache.getline(filename, lineno, opts)
        if not line:
            line = linecache.getline(filename, lineno, proc_obj.curframe.f_globals)
        if line and len(line.strip()) != 0:
            if proc_obj.event:
                print_source_line(intf_obj.msg, lineno, line, proc_obj.event2short[proc_obj.event])
        if '<string>' != filename:
            break

    if proc_obj.event in ['return', 'exception']:
        val = proc_obj.event_arg
        intf_obj.msg('R=> %s' % proc_obj._saferepr(val))
    return True


DEFAULT_PROC_OPTS = {'initfile_list': []}

class CommandProcessor(Mprocessor.Processor):
    __module__ = __name__

    def __init__(self, core_obj, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, DEFAULT_PROC_OPTS)
        Mprocessor.Processor.__init__(self, core_obj)
        self.continue_running = False
        self.event2short = dict(EVENT2SHORT)
        self.event2short['signal'] = '?!'
        self.event2short['brkpt'] = 'xx'
        self.cmd_instances = self._populate_commands()
        self.cmd_argstr = ''
        self.cmd_name = ''
        self.cmd_queue = []
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
        self.prompt_str = '(Pydbgr) '
        self.different_line = None
        self.curframe = None
        self.event = None
        self.event_arg = None
        self.frame = None
        self.list_lineno = 0
        self.macros = {}
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
        initfile_list = get_option('initfile_list')
        for init_cmdfile in initfile_list:
            self.queue_startfile(init_cmdfile)

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
            self.errmsg('No stack.')
            return
        if absolute_pos:
            if pos >= 0:
                pos = len(self.stack) - pos - 1
            else:
                pos = -pos - 1
        else:
            pos += self.curindex
        if pos < 0:
            self.errmsg('Adjusting would put us beyond the oldest frame.')
            return
        elif pos >= len(self.stack):
            self.errmsg('Adjusting would put us beyond the newest frame.')
            return
        self.curindex = pos
        self.curframe = self.stack[self.curindex][0]
        self.location()
        self.list_lineno = None
        return

    def defaultFile(self):
        """Produce a reasonable default."""
        filename = self.curframe.f_code.co_filename
        if filename == '<string>' and self.debugger.mainpyfile:
            filename = self.debugger.mainpyfile
        return filename

    def event_processor(self, frame, event, event_arg, prompt='Pydbgr'):
        """command event processor: reading a commands do something with them."""
        self.frame = frame
        self.event = event
        self.event_arg = event_arg
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno
        if sys.version_info[0] == 2 and sys.version_info[1] <= 4:
            line = None
        else:
            line = linecache.getline(filename, lineno, frame.f_globals)
        if not line:
            opts = {'output': 'plain', 'reload_on_change': self.settings('reload'), 'strip_nl': False}
            line = pyficache.getline(filename, lineno, opts)
        self.current_source_text = line
        if self.settings('skip') is not None:
            if Mbytecode.is_def_stmt(line, frame):
                return True
            if Mbytecode.is_class_def(line, frame):
                return True
        self.thread_name = Mthread.current_thread_name()
        self.frame_thread_name = self.thread_name
        if self.thread_name != 'MainThread':
            prompt += ':' + self.thread_name
        self.prompt_str = '%s%s%s ' % ('(' * self.debug_nest, prompt, ')' * self.debug_nest)
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
            (t, v) = sys.exc_info()[:2]
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
            exec (
             code, global_vars, local_vars)
        except:
            (t, v) = sys.exc_info()[:2]
            if type(t) == str:
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            self.errmsg('%s: %s' % (str(exc_type_name), str(v)))

        return

    def parse_position(self, arg, old_mod=None):
        """parse_position(self, arg)->(fn, name, lineno)

        Parse arg as [filename:]lineno | function | module
        Make sure it works for C:\x0coo\x08ar.py:12
        """
        colon = arg.rfind(':')
        if colon >= 0:
            arg1 = arg[:colon].rstrip()
            lineno_str = arg[colon + 1:].lstrip()
            (mf, filename, lineno) = self.parse_position_one_arg(arg1, old_mod, False)
            if filename is None:
                filename = self.core.canonic(arg1)
            val = self.get_an_int(lineno_str, 'Bad line number: %s' % lineno_str)
            if val is not None:
                lineno = val
        else:
            (mf, filename, lineno) = self.parse_position_one_arg(arg, old_mod)
        return (
         mf, filename, lineno)

    def parse_position_one_arg(self, arg, old_mod=None, show_errmsg=True):
        """parse_position_one_arg(self, arg, show_errmsg) ->
              (module/function, file, lineno)

        See if arg is a line number, function name, or module name.
        Return what we've found. None can be returned as a value in
        the triple.
        """
        (modfunc, filename, lineno) = (None, None, None)
        if self.curframe:
            g = self.curframe.f_globals
            l = self.curframe.f_locals
        else:
            g = globals()
            l = locals()
        try:
            lineno = int(eval(arg, g, l))
            if old_mod is None:
                filename = self.curframe.f_code.co_filename
        except:
            try:
                modfunc = eval(arg, g, l)
            except:
                modfunc = arg
            else:
                msg = ('Object %s is not known yet as a function, module, or is not found' + ' along sys.path, and not a line number.') % str(repr(arg))
                try:
                    if inspect.isfunction(modfunc):
                        pass
                    elif inspect.ismodule(modfunc):
                        filename = Mfile.file_pyc2py(modfunc.__file__)
                        filename = self.core.canonic(filename)
                        return (
                         modfunc, filename, None)
                    elif hasattr(modfunc, 'im_func'):
                        modfunc = modfunc.im_func
                    else:
                        if show_errmsg:
                            self.errmsg(msg)
                        return (None, None, None)
                    code = modfunc.func_code
                    lineno = code.co_firstlineno
                    filename = code.co_filename
                except:
                    if show_errmsg:
                        self.errmsg(msg)
                    return (None, None, None)

        return (
         modfunc, self.core.canonic(filename), lineno)

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
        if min_value and ret_value < min_value:
            self.errmsg('Expecting integer value to be at least %d, got: %d.' % (min_value, ret_value))
            return
        elif max_value and ret_value > max_value:
            self.errmsg('Expecting integer value to be at most %d, got: %d.' % (max_value, ret_value))
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
        default = self.get_int_noerr(arg)
        if default is None:
            if cmdname:
                self.errmsg(("Command '%s' expects an integer; " + 'got: %s.') % (cmdname, str(arg)))
            else:
                self.errmsg('Expecting a positive integer, got: %s' % str(arg))
            return
        if default < min_value:
            if cmdname:
                self.errmsg(("Command '%s' expects an integer at least" + ' %d; got: %d.') % (cmdname, min_value, default))
            else:
                self.errmsg(('Expecting a positive integer at least' + ' %d; got: %d') % (min_value, default))
            return
        elif at_most and default > at_most:
            if cmdname:
                self.errmsg(("Command '%s' expects an integer at most" + ' %d; got: %d.') % (cmdname, at_most, default))
            else:
                self.errmsg('Expecting an integer at most %d; got: %d' % (at_most, default))
        return default

    def getval(self, arg):
        try:
            return eval(arg, self.curframe.f_globals, self.curframe.f_locals)
        except:
            (t, v) = sys.exc_info()[:2]
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
                self.errmsg(Mmisc.wrapped_lines(part1, self.core.execution_status, self.debugger.settings['width']))
                return False
        if self.frame is None and cmd_obj.need_stack:
            self.intf[(-1)].errmsg("Command '%s' needs an execution stack." % name)
            return False
        if nargs < cmd_obj.min_args:
            self.errmsg(("Command '%s' needs at least %d argument(s); " + 'got %d.') % (name, cmd_obj.min_args, nargs))
            return False
        elif cmd_obj.max_args is not None and nargs > cmd_obj.max_args:
            self.errmsg(("Command '%s' can take at most %d argument(s);" + ' got %d.') % (name, cmd_obj.max_args, nargs))
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

    def process_command(self):
        if len(self.cmd_queue) > 0:
            current_command = self.cmd_queue[0].strip()
            del self.cmd_queue[0]
        else:
            current_command = self.intf[(-1)].read_command(self.prompt_str).strip()
            if '' == current_command and self.intf[(-1)].interactive:
                current_command = self.last_command
        if '' == current_command:
            if self.intf[(-1)].interactive:
                self.errmsg('No previous command registered, ' + 'so this is a no-op.')
            return False
        if current_command is None or current_command[0] == '#':
            return False
        try:
            args_list = arg_split(current_command)
        except:
            self.errmsg('bad parse %s' < sys.exc_info()[0])
            return False

        for args in args_list:
            if len(args):
                while True:
                    if len(args) == 0:
                        return False
                    macro_cmd_name = args[0]
                    if macro_cmd_name not in self.macros:
                        break
                    try:
                        current_command = self.macros[macro_cmd_name][0](*args[1:])
                    except TypeError:
                        (t, v) = sys.exc_info()[:2]
                        self.errmsg('Error expanding macro %s' % macro_cmd_name)
                        return False

                    if self.settings('debugmacro'):
                        print current_command
                    if type(current_command) == types.ListType:
                        for x in current_command:
                            if bytes != type(x):
                                self.errmsg(('macro %s should return a List ' + 'of Strings. Has %s of type %s') % (macro_cmd_name, x, repr(current_command), type(x)))
                                return False

                        first = current_command[0]
                        args = first.split()
                        self.cmd_queue + [current_command[1:]]
                        current_command = first
                    elif type(current_command) == str:
                        args = current_command.split()
                    else:
                        self.errmsg(('macro %s should return a List ' + 'of Strings or a String. Got %s') % (macro_cmd_name, repr(current_command)))
                        return False

                self.cmd_name = args[0]
                cmd_name = resolve_name(self, self.cmd_name)
                self.cmd_argstr = current_command[len(self.cmd_name):].lstrip()
                if cmd_name:
                    self.last_command = current_command
                    cmd_obj = self.commands[cmd_name]
                    if self.ok_for_running(cmd_obj, cmd_name, len(args) - 1):
                        try:
                            self.current_command = current_command
                            result = cmd_obj.run(args)
                            if result:
                                return result
                        except (Mexcept.DebuggerQuit, Mexcept.DebuggerRestart, SystemExit):
                            raise
                        except:
                            self.errmsg('INTERNAL ERROR: ' + traceback.format_exc())

                elif not self.settings('autoeval'):
                    self.undefined_cmd(current_command)
                else:
                    self.exec_line(current_command)

        return False

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
        if self.settings('dbg_pydbgr'):
            self.frame = inspect.currentframe()
        if self.event in ['exception', 'c_exception']:
            (exc_type, exc_value, exc_traceback) = self.event_arg
        else:
            (exc_type, exc_value, exc_traceback) = (None, None, None)
        if self.frame or exc_traceback:
            (self.stack, self.curindex) = get_stack(self.frame, exc_traceback, None, self)
            self.curframe = self.stack[self.curindex][0]
            self.thread_name = Mthread.current_thread_name()
        else:
            self.stack = self.curframe = self.botframe = None
        if self.curframe:
            self.list_lineno = max(1, inspect.getlineno(self.curframe) - int(self.settings('listsize') / 2)) - 1
        else:
            self.list_lineno = None
        return False

    def queue_startfile(self, cmdfile):
        """Arrange for file of debugger commands to get read in the
        process-command loop."""
        expanded_cmdfile = os.path.expanduser(cmdfile)
        is_readable = Mfile.readable(expanded_cmdfile)
        if is_readable:
            self.cmd_queue.append('source ' + expanded_cmdfile)
        elif is_readable is None:
            self.errmsg("source file '%s' doesn't exist" % expanded_cmdfile)
        else:
            self.errmsg("source file '%s' is not readable" % expanded_cmdfile)
        return

    def undefined_cmd(self, cmd):
        """Error message when a command doesn't exist"""
        self.errmsg('Undefined command: "%s". Try "help".' % cmd)

    def write_history_file(self):
        """Write the command history file -- possibly."""
        settings = self.debugger.settings
        if settings['hist_save']:
            try:
                import readline
                try:
                    readline.write_history_file(settings['histfile'])
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
        cmd_instances = []
        Mcommand = import_relative('command')
        eval_cmd_template = 'command_mod.%s(self)'
        srcdir = get_srcdir()
        sys.path.insert(0, srcdir)
        for mod_name in Mcommand.__modules__:
            if mod_name in ('info_sub', 'set_sub', 'show_sub'):
                pass
            import_name = 'command.' + mod_name
            if False:
                command_mod = getattr(__import__(import_name), mod_name)
            else:
                command_mod = getattr(__import__(import_name), mod_name)
                try:
                    command_mod = getattr(__import__(import_name), mod_name)
                except:
                    print 'Error importing %s: %s' % (mod_name, sys.exc_info()[0])
                    continue

            classnames = [ tup[0] for tup in inspect.getmembers(command_mod, inspect.isclass) if 'DebuggerCommand' != tup[0] if tup[0].endswith('Command') ]
            for classname in classnames:
                eval_cmd = eval_cmd_template % classname
                if True:
                    instance = eval(eval_cmd)
                    cmd_instances.append(instance)
                else:
                    try:
                        instance = eval(eval_cmd)
                        cmd_instances.append(instance)
                    except:
                        print 'Error loading %s from %s: %s' % (classname, mod_name, sys.exc_info()[0])

        sys.path.remove(srcdir)
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
    Mmock = import_relative('command.mock')
    d = Mmock.MockDebugger()
    cmdproc = CommandProcessor(d.core)
    print 'commands:'
    commands = list(cmdproc.commands.keys())
    commands.sort()
    print commands
    print 'aliases:'
    aliases = list(cmdproc.aliases.keys())
    aliases.sort()
    print aliases
    print resolve_name(cmdproc, 'quit')
    print resolve_name(cmdproc, 'q')
    print resolve_name(cmdproc, 'info')
    print resolve_name(cmdproc, 'i')
    cmdproc.frame = sys._getframe()
    cmdproc.setup()
    print ()
    print '-' * 10
    cmdproc.location()
    print '-' * 10
    print cmdproc.eval('1+2')
    print cmdproc.eval('len(aliases)')
    import pprint
    print pprint.pformat(cmdproc.category)
    print arg_split('Now is the time')
    print arg_split('Now is the time ;;')
    print arg_split("Now is 'the time'")
    print arg_split('Now is the time ;; for all good men')
    print arg_split("Now is the time ';;' for all good men")
    print cmdproc.parse_position_one_arg('4+1')
    print cmdproc.parse_position_one_arg('os.path')
    print cmdproc.parse_position_one_arg('os.path.join')
    print cmdproc.parse_position_one_arg('/bin/bash', show_errmsg=False)
    print cmdproc.parse_position('/bin/bash')
    print cmdproc.parse_position('/bin/bash:4')
    print cmdproc.commands
    fn = cmdproc.commands['quit']
    print 'Removing non-existing quit hook: %s' % cmdproc.remove_preloop_hook(fn)
    cmdproc.add_preloop_hook(fn)
    print cmdproc.preloop_hooks
    print 'Removed existing quit hook: %s' % cmdproc.remove_preloop_hook(fn)