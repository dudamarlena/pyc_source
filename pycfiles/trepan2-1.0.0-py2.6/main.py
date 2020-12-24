# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/bwprocessor/main.py
# Compiled at: 2015-02-16 15:47:50
import inspect, linecache, sys, traceback, types, pyficache
from repr import Repr
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
        self.response = {'errs': [], 'msg': []}
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
            exec code in global_vars, local_vars
        except:
            (t, v) = sys.exc_info()[:2]
            if isinstance(t, types.StringType):
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

    def process_command(self):
        self.response = {'errs': [], 'msg': []}
        cmd_hash = self.intf[(-1)].read_command()
        if isinstance(cmd_hash, types.DictType):
            Mmsg.errmsg(self, 'invalid input, expecting a hash: %s' % cmd_hash, {'set_name': True})
            self.intf[(-1)].msg(self.response)
            return False
        if 'command' not in cmd_hash:
            Mmsg.errmsg(self, "invalid input, expecting a 'command' key: %s" % cmd_hash, {'set_name': True})
            self.intf[(-1)].msg(self.response)
            return False
        self.cmd_name = cmd_hash['command']
        cmd_name = resolve_name(self, self.cmd_name)
        if cmd_name:
            cmd_obj = self.commands[cmd_name]
            if self.ok_for_running(cmd_obj, cmd_name, cmd_hash):
                try:
                    self.response['name'] = cmd_name
                    result = cmd_obj.run(cmd_hash)
                    self.intf[(-1)].msg(self.response)
                    if result:
                        return result
                except (Mexcept.DebuggerQuit,
                 Mexcept.DebuggerRestart, SystemExit):
                    raise
                except:
                    Mmsg.errmsg(self, 'INTERNAL ERROR: ' + traceback.format_exc())

            else:
                self.undefined_cmd(cmd_name)
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
        if self.settings('dbg_trepan'):
            self.frame = inspect.currentframe()
        if self.event in ('exception', 'c_exception'):
            (exc_type, exc_value, exc_traceback) = self.event_arg
        else:
            (_, _, exc_traceback) = (None, None, None)
        if self.frame or exc_traceback:
            (self.stack, self.curindex) = get_stack(self.frame, exc_traceback, None, self)
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
                print 'Error importing %s: %s' % (
                 mod_name, sys.exc_info()[0])
                continue

            classnames = [ tup[0] for tup in inspect.getmembers(command_mod, inspect.isclass) if 'DebuggerCommand' != tup[0] if tup[0].endswith('Command')
                         ]
            for classname in classnames:
                eval_cmd = eval_cmd_template % classname
                try:
                    instance = eval(eval_cmd)
                    cmd_instances.append(instance)
                except:
                    print 'Error loading %s from %s: %s' % (
                     classname, mod_name, sys.exc_info()[0])

        return cmd_instances

    def _populate_cmd_lists(self):
        """ Populate self.commands"""
        self.commands = {}
        for cmd_instance in self.cmd_instances:
            cmd_name = cmd_instance.name
            self.commands[cmd_name] = cmd_instance


if __name__ == '__main__':
    from trepan.interfaces import bullwinkle as Mbullwinkle

    class Debugger():

        def __init__(self):
            self.intf = [
             Mbullwinkle.BWInterface()]
            self.settings = {'dbg_trepan': True, 'reload': False}


    class MockCore():

        def filename(self, fn):
            return fn

        def canonic_filename(self, frame):
            return frame.f_code.co_filename

        def __init__(self):
            self.debugger = Debugger()


    core = MockCore()
    bwproc = BWProcessor(core)
    print 'commands:'
    commands = bwproc.commands.keys()
    commands.sort()
    print commands
    print resolve_name(bwproc, 'quit')
    bwproc.frame = sys._getframe()
    bwproc.setup()
    Mlocation.print_location(bwproc)