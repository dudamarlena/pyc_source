# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/threads.py
# Compiled at: 2013-03-24 01:17:04
import sys, threading
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mstack = import_relative('stack', '....lib', 'pydbgr')
Mthread = import_relative('thread', '....lib', 'pydbgr')

class InfoThread(Mbase_subcmd.DebuggerSubcommand):
    """info threads [thread-name|thread-number] [terse|verbose]
    List all currently-known thread name(s).
    
If no thread name is given, we list info for all threads. Unless a
terse listing, for each thread we give:

  - the class, thread name, and status as <Class(Thread-n, status)>
  - the top-most call-stack information for that thread. Generally
    the top-most calls into the debugger and dispatcher are omitted unless
    set dbg_pydbgr is True.

    If 'verbose' appended to the end of the command, then the entire
    stack trace is given for each frame.
    If 'terse' is appended we just list the thread name and thread id.

To get the full stack trace for a specific thread pass in the thread name.
"""
    __module__ = __name__
    min_abbrev = 2
    need_stack = True
    short_help = 'List thread info'

    def __init__(self, cmd):
        Mbase_subcmd.DebuggerSubcommand.__init__(self, cmd)
        self.name2id = {}

    def stack_trace(self, f):
        """A mini stack trace routine for threads."""
        while f:
            if not self.core.ignore_filter.is_included(f) or self.settings['dbg_pydbgr']:
                s = Mstack.format_stack_entry(self, (f, f.f_lineno))
                self.msg(' ' * 4 + s)
            f = f.f_back

    def info_thread_terse(self, name2id, arg=None):
        if arg is not None:
            thread_name = arg
            if thread_name in list(name2id.keys()):
                self.info_thread_line(thread_name, name2id)
            else:
                self.errmsg("Don't know about thread name %s" % thread_name)
                return
        thread_name_list = list(name2id.keys())
        thread_name_list.sort()
        for thread_name in thread_name_list:
            self.info_thread_line(thread_name, name2id)

        return

    def info_thread_line(self, thread_name, name2id):
        if thread_name == self.proc.frame_thread_name:
            prefix = '-> '
        elif thread_name == self.proc.thread_name:
            prefix = '=> '
        else:
            prefix = '   '
        self.msg('%s%s: %d' % (prefix, thread_name, name2id[thread_name]))

    def run(self, args):
        self.thread_name = Mthread.current_thread_name()
        name2id = Mthread.map_thread_names()
        for thread_id in list(threading._active.keys()):
            thread = threading._active[thread_id]
            name = thread.getName()
            if name not in list(self.name2id.keys()):
                self.name2id[name] = thread_id

        all_verbose = False
        if len(args) == 1:
            if args[0].startswith('verbose'):
                all_verbose = True
            elif args[0].startswith('terse'):
                self.info_thread_terse(name2id)
                return
        if len(args) > 0 and not all_verbose:
            thread_name = args[0]
            if thread_name == '.':
                thread_name = self.thread_name
            try:
                thread_id = int(thread_name)
                if thread_id not in list(threading._active.keys()):
                    self.errmsg("Don't know about thread number %s" % thread_name)
                    self.info_thread_terse(name2id)
                    return
            except ValueError:
                if thread_name not in list(self.name2id.keys()):
                    self.errmsg("Don't know about thread %s" % thread_name)
                    self.info_thread_terse(name2id)
                    return
                thread_id = self.name2id[thread_name]
            else:
                frame = sys._current_frames()[thread_id]
                self.stack_trace(frame)
                return
        thread_key_list = list(self.name2id.keys())
        thread_key_list.sort()
        for thread_name in thread_key_list:
            thread_id = self.name2id[thread_name]
            frame = sys._current_frames()[thread_id]
            s = ''
            if thread_id in threading._active:
                thread = threading._active[thread_id]
                thread_name = thread.getName()
                if thread_name == self.proc.frame_thread_name:
                    prefix = '-> '
                    if not self.settings['dbg_pydbgr']:
                        frame = Mthread.find_debugged_frame(frame)
                elif thread_name == self.proc.thread_name:
                    prefix = '=> '
                else:
                    prefix = '   '
                s += '%s%s' % (prefix, str(thread))
                if all_verbose:
                    s += ': %d' % thread_id
            else:
                s += '    thread id: %d' % thread_id
            s += '\n    '
            s += Mstack.format_stack_entry(self, (frame, frame.f_lineno))
            self.msg('-' * 40)
            self.msg(s)
            frame = frame.f_back
            if all_verbose and frame:
                self.stack_trace(frame)


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoThread(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])
    print '=' * 30
    sub.run(['foo'])
    print '=' * 30
    sub.run(['MainThread'])
    print '=' * 30
    sub.run(['terse'])
    print '=' * 30
    sub.run(['verbose'])
    print '=' * 30
    sub.run(['MainThread', 'verbose'])