# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/lib/sighandler.py
# Compiled at: 2016-01-13 01:46:34
"""Signal handlers."""
import signal

def YN(b):
    """Return 'Yes' for True and 'No' for False, and ?? for anything
    else."""
    if type(b) != bool:
        return '??'
    if b:
        return 'Yes'
    return 'No'


def lookup_signame(num):
    """Find the corresponding signal name for 'num'. Return None
    if 'num' is invalid."""
    signames = signal.__dict__
    num = abs(num)
    for signame in list(signames.keys()):
        if signame.startswith('SIG') and signames[signame] == num:
            return signame

    return


def lookup_signum(name):
    """Find the corresponding signal number for 'name'. Return None
    if 'name' is invalid."""
    uname = name.upper()
    if uname.startswith('SIG') and hasattr(signal, uname):
        return getattr(signal, uname)
    else:
        uname = 'SIG' + uname
        if hasattr(signal, uname):
            return getattr(signal, uname)
        else:
            return
        return


def canonic_signame(name_num):
    """Return a signal name for a signal name or signal
    number.  Return None is name_num is an int but not a valid signal
    number and False if name_num is a not number. If name_num is a
    signal name or signal number, the canonic if name is returned."""
    signum = lookup_signum(name_num)
    if signum is None:
        try:
            num = int(name_num)
            signame = lookup_signame(num)
            if signame is None:
                return
        except:
            return False

        return signame
    else:
        signame = name_num.upper()
        if not signame.startswith('SIG'):
            return 'SIG' + signame
        return signame


fatal_signals = ['SIGKILL', 'SIGSTOP']
signal_description = {'SIGHUP': 'Hangup', 
 'SIGINT': 'Interrupt', 
 'SIGQUIT': 'Quit', 
 'SIGILL': 'Illegal instruction', 
 'SIGTRAP': 'Trace/breakpoint trap', 
 'SIGABRT': 'Aborted', 
 'SIGEMT': 'Emulation trap', 
 'SIGFPE': 'Arithmetic exception', 
 'SIGKILL': 'Killed', 
 'SIGBUS': 'Bus error', 
 'SIGSEGV': 'Segmentation fault', 
 'SIGSYS': 'Bad system call', 
 'SIGPIPE': 'Broken pipe', 
 'SIGALRM': 'Alarm clock', 
 'SIGTERM': 'Terminated', 
 'SIGURG': 'Urgent I/O condition', 
 'SIGSTOP': 'Stopped (signal)', 
 'SIGTSTP': 'Stopped (user)', 
 'SIGCONT': 'Continued', 
 'SIGCHLD': 'Child status changed', 
 'SIGTTIN': 'Stopped (tty input)', 
 'SIGTTOU': 'Stopped (tty output)', 
 'SIGIO': 'I/O possible', 
 'SIGXCPU': 'CPU time limit exceeded', 
 'SIGXFSZ': 'File size limit exceeded', 
 'SIGVTALRM': 'Virtual timer expired', 
 'SIGPROF': 'Profiling timer expired', 
 'SIGWINCH': 'Window size changed', 
 'SIGLOST': 'Resource lost', 
 'SIGUSR1': 'User-defined signal 1', 
 'SIGUSR2': 'User-defined signal 2', 
 'SIGPWR': 'Power fail/restart', 
 'SIGPOLL': 'Pollable event occurred', 
 'SIGWIND': 'SIGWIND', 
 'SIGPHONE': 'SIGPHONE', 
 'SIGWAITING': "Process's LWPs are blocked", 
 'SIGLWP': 'Signal LWP', 
 'SIGDANGER': 'Swap space dangerously low', 
 'SIGGRANT': 'Monitor mode granted', 
 'SIGRETRACT': 'Need to relinquish monitor mode', 
 'SIGMSG': 'Monitor mode data available', 
 'SIGSOUND': 'Sound completed', 
 'SIGSAK': 'Secure attention'}

class SignalManager:
    """Manages Signal Handling information for the debugger

    - Do we print/not print when signal is caught
    - Do we pass/not pass the signal to the program
    - Do we stop/not stop when signal is caught

    Parameter dbgr is a Debugger object. ignore is a list of
    signals to ignore. If you want no signals, use [] as None uses the
    default set. Parameter default_print specifies whether or not we
    print receiving a signals that is not ignored.

    All the methods which change these attributes return None on error, or
    True/False if we have set the action (pass/print/stop) for a signal
    handler.
    """

    def __init__(self, dbgr, ignore_list=None, default_print=True):
        self.dbgr = dbgr
        self.sigs = {}
        self.siglist = []
        if ignore_list is None:
            ignore_list = [
             'SIGALRM', 'SIGCHLD', 'SIGURG',
             'SIGIO', 'SIGCLD',
             'SIGVTALRMSIGPROF', 'SIGWINCH', 'SIGPOLL',
             'SIGWAITING', 'SIGLWP', 'SIGCANCEL', 'SIGTRAP',
             'SIGTERM', 'SIGQUIT', 'SIGILL',
             'SIG_SETMASK', 'ITIMER_PROF', 'ITIMER_VIRTUAL',
             'ITIMER_REAL', 'ITIMER_PROF',
             'SIG_BLOCK', 'SIG_UNBLOCK']
        self.ignore_list = ignore_list
        self._orig_set_signal = signal.signal
        signal.signal = self.set_signal_replacement
        self.info_fmt = '%-14s%-4s\t%-4s\t%-5s\t%-4s\t%s'
        self.header = self.info_fmt % ('Signal', 'Stop', 'Print', 'Stack', 'Pass',
                                       'Description')
        if default_print:
            default_print = self.dbgr.intf[(-1)].msg
        for signame in list(signal.__dict__.keys()):
            if signame.startswith('SIG') and '_' not in signame:
                self.siglist.append(signame)
                self.initialize_handler(signame)
                continue

        self.action('SIGINT stop print nostack nopass')
        return

    def initialize_handler(self, signame):
        if signame in fatal_signals:
            return False
        else:
            signum = lookup_signum(signame)
            if signum is None:
                return False
            try:
                old_handler = signal.getsignal(signum)
            except ValueError:
                old_handler = None
                if signame in self.sigs:
                    self.sigs.pop(signame)

            if signame in self.ignore_list:
                self.sigs[signame] = SigHandler(self.dbgr, signame, signum, old_handler, None, False, print_stack=False, pass_along=True)
            else:
                self.sigs[signame] = SigHandler(self.dbgr, signame, signum, old_handler, self.dbgr.intf[(-1)].msg, True, print_stack=False, pass_along=False)
            return True

    def set_signal_replacement(self, signum, handle):
        """A replacement for signal.signal which chains the signal behind
        the debugger's handler"""
        signame = lookup_signame(signum)
        if signame is None:
            self.dbgr.intf[(-1)].errmsg('%s is not a signal number I know about.' % signum)
            return False
        else:
            self.sigs[signame].pass_along = True
            if self.check_and_adjust_sighandler(signame, self.sigs):
                self.sigs[signame].old_handler = handle
                return True
            return False

    def check_and_adjust_sighandler(self, signame, sigs):
        """
        Check to see if a single signal handler that we are interested
        in has changed or has not been set initially. On return
        self.sigs[signame] should have our signal handler. True is
        returned if the same or adjusted, False or None if error or
        not found.
        """
        signum = lookup_signum(signame)
        try:
            old_handler = signal.getsignal(signum)
        except ValueError:
            if signame in self.sigs:
                sigs.pop(signame)
            return

        if old_handler != self.sigs[signame].handle:
            if old_handler not in [signal.SIG_IGN, signal.SIG_DFL]:
                sigs[signame].old_handler = old_handler
            try:
                self._orig_set_signal(signum, self.sigs[signame].handle)
            except ValueError:
                return False
            except KeyError:
                return False

        return True

    def check_and_adjust_sighandlers(self):
        """Check to see if any of the signal handlers we are interested in have
        changed or is not initially set. Change any that are not right. """
        for signame in list(self.sigs.keys()):
            if not self.check_and_adjust_sighandler(signame, self.sigs):
                break

    def is_name_or_number(self, name_num):
        signame = canonic_signame(name_num)
        if signame is None:
            self.dbgr.intf[(-1)].errmsg(('%s is not a signal number' + ' I know about.') % name_num)
            return False
        else:
            if not signame:
                self.dbgr.intf[(-1)].errmsg(('%s is not a signal name I ' + 'know about.') % name_num)
                return False
            return signame

    def print_info_signal_entry(self, signame):
        """Print status for a single signal name (signame)"""
        if signame in signal_description:
            description = signal_description[signame]
        else:
            description = ''
        if signame not in list(self.sigs.keys()):
            self.dbgr.intf[(-1)].msg(self.info_fmt % (
             signame, 'No', 'No', 'No', 'Yes',
             description))
            return
        else:
            sig_obj = self.sigs[signame]
            self.dbgr.intf[(-1)].msg(self.info_fmt % (
             signame,
             YN(sig_obj.b_stop),
             YN(sig_obj.print_method is not None),
             YN(sig_obj.print_stack),
             YN(sig_obj.pass_along),
             description))
            return

    def info_signal(self, args):
        """Print information about a signal"""
        if len(args) == 0:
            return None
        else:
            signame = args[0]
            if signame in ('handle', 'signal'):
                if len(args) == 1:
                    self.dbgr.core.processor.section(self.header)
                    for signame in self.siglist:
                        self.print_info_signal_entry(signame)

                    return True
                signame = args[1]
            signame = self.is_name_or_number(signame)
            self.dbgr.core.processor.section(self.header)
            self.print_info_signal_entry(signame)
            return True

    def action(self, arg):
        """Delegate the actions specified in 'arg' to another
        method.
        """
        if not arg:
            self.info_signal(['handle'])
            return True
        else:
            args = arg.split()
            signame = args[0]
            signame = self.is_name_or_number(args[0])
            if not signame:
                return
            else:
                if len(args) == 1:
                    self.info_signal([signame])
                    return True
                if signame in fatal_signals:
                    pass
                return
            if signame not in list(self.sigs.keys()):
                if not self.initialize_handler(signame):
                    return
            for attr in args[1:]:
                if attr.startswith('no'):
                    on = False
                    attr = attr[2:]
                else:
                    on = True
                if 'stop'.startswith(attr):
                    self.handle_stop(signame, on)
                elif 'print'.startswith(attr) and len(attr) >= 2:
                    self.handle_print(signame, on)
                elif 'pass'.startswith(attr):
                    self.handle_pass(signame, on)
                elif 'ignore'.startswith(attr):
                    self.handle_ignore(signame, on)
                elif 'stack'.startswith(attr):
                    self.handle_print_stack(signame, on)
                else:
                    self.dbgr.intf[(-1)].errmsg('Invalid arguments')

            return self.check_and_adjust_sighandler(signame, self.sigs)

    def handle_print_stack(self, signame, print_stack):
        """Set whether we stop or not when this signal is caught.
        If 'set_stop' is True your program will stop when this signal
        happens."""
        self.sigs[signame].print_stack = print_stack
        return print_stack

    def handle_stop(self, signame, set_stop):
        """Set whether we stop or not when this signal is caught.
        If 'set_stop' is True your program will stop when this signal
        happens."""
        if set_stop:
            self.sigs[signame].b_stop = True
            self.sigs[signame].print_method = self.dbgr.intf[(-1)].msg
            self.sigs[signame].pass_along = False
        else:
            self.sigs[signame].b_stop = False
        return set_stop

    def handle_pass(self, signame, set_pass):
        """Set whether we pass this signal to the program (or not)
        when this signal is caught. If set_pass is True, Dbgr should allow
        your program to see this signal.
        """
        self.sigs[signame].pass_along = set_pass
        if set_pass:
            self.sigs[signame].b_stop = False
        return set_pass

    def handle_ignore(self, signame, set_ignore):
        """'pass' and 'noignore' are synonyms. 'nopass and 'ignore' are
        synonyms."""
        self.handle_pass(signame, not set_ignore)
        return set_ignore

    def handle_print(self, signame, set_print):
        """Set whether we print or not when this signal is caught."""
        if set_print:
            self.sigs[signame].print_method = self.dbgr.intf[(-1)].msg
        else:
            self.sigs[signame].print_method = None
        return set_print


class SigHandler:
    """Store information about what we do when we handle a signal,

    - Do we print/not print when signal is caught
    - Do we pass/not pass the signal to the program
    - Do we stop/not stop when signal is caught

    Parameters:
       signame : name of signal (e.g. SIGUSR1 or USR1)
       print_method routine to use for "print"
       stop routine to call to invoke debugger when stopping
       pass_along: True is signal is to be passed to user's handler
    """

    def __init__(self, dbgr, signame, signum, old_handler, print_method, b_stop, print_stack=False, pass_along=True):
        self.dbgr = dbgr
        self.old_handler = old_handler
        self.pass_along = pass_along
        self.print_method = print_method
        self.print_stack = print_stack
        self.signame = signame
        self.signum = signum
        self.b_stop = b_stop

    def handle(self, signum, frame):
        """This method is called when a signal is received."""
        if self.print_method:
            self.print_method('\nProgram received signal %s.' % self.signame)
        if self.print_stack:
            import traceback
            strings = traceback.format_stack(frame)
            for s in strings:
                if s[(-1)] == '\n':
                    s = s[0:-1]
                self.print_method(s)

        if self.b_stop:
            core = self.dbgr.core
            old_trace_hook_suspend = core.trace_hook_suspend
            core.trace_hook_suspend = True
            core.stop_reason = 'intercepting signal %s (%d)' % (
             self.signame, signum)
            core.processor.event_processor(frame, 'signal', signum)
            core.trace_hook_suspend = old_trace_hook_suspend
        if self.pass_along:
            if self.old_handler:
                self.old_handler(signum, frame)


if __name__ == '__main__':
    import trepan.inout, trepan.processor.command, trepan.interfaces
    for b in (True, False):
        print('YN of %s is %s' % (repr(b), YN(b)))

    for signum in range(signal.NSIG):
        signame = lookup_signame(signum)
        if signame is not None:
            if not signame.startswith('SIG'):
                continue
            print(signame, signum, lookup_signum(signame))
            assert signum == lookup_signum(signame)
            assert signum == lookup_signum(signame[3:])

    for i in (15, -15, 300):
        print('lookup_signame(%d): %s' % (i, lookup_signame(i)))

    for i in ('term', 'TERM', 'NotThere'):
        print('lookup_signum(%s): %s' % (i, repr(lookup_signum(i))))

    for i in ('15', '-15', 'term', 'sigterm', 'TERM', '300', 'bogus'):
        print('canonic_signame(%s): %s' % (i, canonic_signame(i)))

    from trepan import debugger as Mdebugger
    dbgr = Mdebugger.Trepan()
    h = SignalManager(dbgr)
    h.info_signal(['TRAP'])
    h.action('SIGUSR1')
    h.action('usr1 print pass stop')
    h.info_signal(['USR1'])
    h.action('SIGUSR1 noprint')
    h.info_signal(['USR1'])
    h.action('foo nostop')
    h.action('SIGUSR1 stop')
    h.info_signal(['SIGUSR1'])
    h.action('SIGUSR1 noprint')
    h.info_signal(['SIGUSR1'])
    h.action('SIGUSR1 nopass stack')
    h.info_signal(['SIGUSR1'])