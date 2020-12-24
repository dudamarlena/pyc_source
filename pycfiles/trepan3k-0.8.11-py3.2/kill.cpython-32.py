# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/kill.py
# Compiled at: 2017-06-03 21:37:52
import os, signal, sys, time
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import complete as Mcomplete
if sys.platform != 'win32':
    kill = os.kill
    sleep = time.sleep
else:
    import threading
    sigmap = {signal.SIGINT: signal.CTRL_C_EVENT,  signal.SIGBREAK: signal.CTRL_BREAK_EVENT}

    def kill(pid, signum):
        if signum in sigmap and pid == os.getpid():
            pid = 0
        thread = threading.current_thread()
        handler = signal.getsignal(signum)
        if signum in sigmap and thread.name == 'MainThread' and callable(handler) and pid == 0:
            event = threading.Event()

            def handler_set_event(signum, frame):
                event.set()
                return handler(signum, frame)

            signal.signal(signum, handler_set_event)
            try:
                kill(pid, sigmap[signum])
                while not event.is_set():
                    pass

            finally:
                signal.signal(signum, handler)

        else:
            kill(pid, sigmap.get(signum, signum))


    if sys.version_info[0] > 2:
        sleep = time.sleep
    else:
        import errno

        def sleep(interval):
            """sleep that ignores EINTR in 2.x on Windows"""
            while 1:
                try:
                    t = time.time()
                    time.sleep(interval)
                except IOError as e:
                    if e.errno != errno.EINTR:
                        raise

                interval -= time.time() - t
                if interval <= 0:
                    break


class KillCommand(Mbase_cmd.DebuggerCommand):
    """**kill** [ *signal-number* ] [unconditional]

Send this process a POSIX signal ('9' for 'SIGKILL' or 'kill -SIGKILL')

9 is a non-maskable interrupt that terminates the program. If program
is threaded it may be expedient to use this command to terminate the program.

However other signals, such as those that allow for the debugged to
handle them can be sent.

Giving a negative number is the same as using its
positive value.

Examples:
--------

    kill                # non-interuptable, nonmaskable kill
    kill 9              # same as above
    kill -9             # same as above
    kill!               # same as above, but no confirmation
    kill unconditional  # same as above
    kill 15             # nicer, maskable TERM signal
    kill! 15            # same as above, but no confirmation

See also:
---------

`quit` for less a forceful termination command; `exit` for another way to force termination.

`run` and `restart` are ways to restart the debugged program.
"""
    aliases = ('kill!', )
    category = 'running'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Send this process a POSIX signal ("9" for "kill -9")'

    def complete(self, prefix):
        names = [sig for sig in signal.__dict__.keys() if sig.startswith('SIG')]
        nums = [str(eval('signal.' + name)) for name in names]
        lnames = [sig.lower() for sig in names]
        completions = lnames + nums + ['unconditional']
        return Mcomplete.complete_token(completions, prefix.lower())

    def run(self, args):
        if sys.platform != 'win32':
            signo = signal.SIGKILL
        else:
            signo = signal.CTRL_BREAK_EVENT
        confirmed = False
        if len(args) <= 1:
            if '!' != args[0][(-1)]:
                confirmed = self.confirm('Really do a hard kill', False)
            else:
                confirmed = True
        else:
            if 'unconditional'.startswith(args[1]):
                confirmed = True
            else:
                try:
                    signo = abs(int(args[1]))
                    confirmed = True
                except ValueError:
                    pass

        if confirmed:
            import os
            kill(os.getpid(), signo)
        return False


if __name__ == '__main__':

    def handle(*args):
        print('signal received')


    signal.signal(28, handle)
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = KillCommand(cp)
    print(command.complete(''))
    command.run(['kill', 'wrong', 'number', 'of', 'args'])
    command.run(['kill', '28'])
    command.run(['kill!'])