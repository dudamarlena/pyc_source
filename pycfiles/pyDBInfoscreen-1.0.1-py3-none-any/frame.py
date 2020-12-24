# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/frame.py
# Compiled at: 2013-03-12 21:41:19
import inspect, os, sys, threading
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', '.', 'pydbgr')
Mcmdproc = import_relative('cmdproc', '..', 'pydbgr')
Mthread = import_relative('thread', '...lib', 'pydbgr')

class FrameCommand(Mbase_cmd.DebuggerCommand):
    """**frame** [*thread-Name*|*thread-number*] [*frame-number*]
    
Change the current frame to frame *frame-number* if specified, or the
current frame, 0, if no frame number specified.

If a thread name or thread number is given, change the current frame
to a frame in that thread. Dot (.) can be used to indicate the name of
the current frame the debugger is stopped in.

A negative number indicates the position from the other or 
least-recently-entered end.  So `frame -1` moves to the oldest frame,
and `frame 0` moves to the newest frame. Any variable or expression
that evaluates to a number can be used as a position, however due to
parsing limitations, the position expression has to be seen as a single
blank-delimited parameter. That is, the expression `(5*3)-1` is okay
while `(5 * 3) - 1)` isn't.

**Examples:**

   frame     # Set current frame at the current stopping point
   frame 0   # Same as above
   frame 5-5 # Same as above. Note: no spaces allowed in expression 5-5
   frame .   # Same as above. "current thread" is explicit.
   frame . 0 # Same as above.
   frame 1   # Move to frame 1. Same as: frame 0; up
   frame -1  # The least-recent frame
   frame MainThread 0 # Switch to frame 0 of thread MainThread
   frame MainThread   # Same as above
   frame -2434343 0   # Use a thread number instead of name

See also `up`, `down`, `backtrace`, and `info thread`.
"""
    __module__ = __name__
    category = 'stack'
    min_args = 0
    max_args = 2
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Select and print a stack frame'

    def find_and_set_debugged_frame(self, frame, thread_id):
        """The dance we have to do to set debugger frame state to
        *frame*, which is in the thread with id *thread_id*. We may
        need to the hide initial debugger frames.
        """
        thread = threading._active[thread_id]
        thread_name = thread.getName()
        if not self.settings['dbg_pydbgr'] and thread_name == Mthread.current_thread_name():
            newframe = Mthread.find_debugged_frame(frame)
            if newframe is not None:
                frame = newframe
        (self.stack, self.curindex) = Mcmdproc.get_stack(frame, None, self.proc)
        self.proc.stack, self.proc.curindex = self.stack, self.curindex
        self.proc.frame_thread_name = thread_name
        return

    def one_arg_run(self, position_str):
        """The simple case: thread frame switching has been done or is
        not needed and we have an explicit position number as a string"""
        frame_num = self.proc.get_an_int(position_str, ("The 'frame' command requires a" + ' frame number. Got: %s') % position_str)
        if frame_num is None:
            return False
        i_stack = len(self.proc.stack)
        if i_stack == 0:
            self.errmsg('No frames recorded')
            return False
        if frame_num < -i_stack or frame_num > i_stack - 1:
            self.errmsg(('Frame number has to be in the range %d to %d.' + ' Got: %d (%s).') % (-i_stack, i_stack - 1, frame_num, position_str))
            return False
        else:
            self.proc.adjust_frame(pos=frame_num, absolute_pos=True)
            return True
        return

    def get_from_thread_name_or_id(self, name_or_id, report_error=True):
        """See if *name_or_id* is either a thread name or a thread id.
        The frame of that id/name is returned, or None if name_or_id is
        invalid."""
        thread_id = self.proc.get_int_noerr(name_or_id)
        if thread_id is None:
            name2id = Mthread.map_thread_names()
            if name_or_id == '.':
                name_or_id = Mthread.current_thread_name()
            thread_id = name2id.get(name_or_id)
            if thread_id is None:
                self.errmsg("I don't know about thread name %s." % name_or_id)
                return (None, None)
        threads = sys._current_frames()
        frame = threads.get(thread_id)
        if frame is None and report_error:
            self.errmsg("I don't know about thread number %s (%d)." % name_or_id, thread_id)
            return (None, None)
        return (frame, thread_id)

    def run(self, args):
        """Run a frame command. This routine is a little complex
        because we allow a number parameter variations."""
        if len(args) == 1:
            position_str = '0'
        elif len(args) == 2:
            name_or_id = args[1]
            (frame, thread_id) = self.get_from_thread_name_or_id(name_or_id, False)
            if frame is None:
                position_str = name_or_id
            else:
                position_str = '0'
                self.find_and_set_debugged_frame(frame, thread_id)
        elif len(args) == 3:
            name_or_id = args[1]
            position_str = args[2]
            (frame, thread_id) = self.get_from_thread_name_or_id(name_or_id)
            if frame is None:
                return
            self.find_and_set_debugged_frame(frame, thread_id)
        self.one_arg_run(position_str)
        return False


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...', 'pydbgr')
    d = Mdebugger.Debugger()
    cp = d.core.processor
    command = FrameCommand(cp)
    command.run(['frame'])
    command.run(['frame', '1'])
    print '=' * 20
    cp.curframe = inspect.currentframe()
    (cp.stack, cp.curindex) = Mcmdproc.get_stack(cp.curframe, None, None, cp)

    def showit(cmd):
        print '=' * 20
        cmd.run(['frame'])
        print '-' * 20
        cmd.run(['frame', 'MainThread'])
        print '-' * 20
        cmd.run(['frame', '.', '0'])
        print '-' * 20
        cmd.run(['frame', '.'])
        print '=' * 20


    class BgThread(threading.Thread):
        __module__ = __name__

        def __init__(self, fn, cmd):
            threading.Thread.__init__(self)
            self.fn = fn
            self.cmd = cmd

        def run(self):
            self.fn(self.cmd)


    background = BgThread(showit, command)
    background.start()
    background.join()