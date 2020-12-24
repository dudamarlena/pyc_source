# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interfaces/user.py
# Compiled at: 2017-08-12 23:13:24
"""Interface when communicating with the user in the same process as
    the debugged program."""
import atexit, os
from trepan import interface as Minterface
histfile = os.path.expanduser('~/.trepan_hist')
DEFAULT_USER_SETTINGS = {'histfile': histfile, 'complete': None}
try:
    from readline import read_history_file, set_completer, set_history_length
    from readline import write_history_file, parse_and_bind
except ImportError:
    pass

class UserInterface(Minterface.DebuggerInterface):
    """Interface when communicating with the user in the same
    process as the debugged program."""
    __module__ = __name__

    def __init__(self, inp=None, out=None, opts={}):
        user_opts = DEFAULT_USER_SETTINGS.copy()
        user_opts.update(opts)
        from trepan.inout import input as Minput, output as Moutput
        atexit.register(self.finalize)
        self.interactive = True
        self.input = inp or Minput.DebuggerUserInput()
        self.output = out or Moutput.DebuggerUserOutput()
        if self.input.use_history():
            self.complete = user_opts['complete']
            if self.complete:
                parse_and_bind('tab: complete')
                set_completer(self.complete)
            self.histfile = user_opts['histfile']
            if self.histfile:
                try:
                    read_history_file(histfile)
                except IOError:
                    pass
                except:
                    return
                else:
                    set_history_length(50)
                    atexit.register(write_history_file, self.histfile)

    def close(self):
        """ Closes both input and output """
        if not self.input.closed:
            self.input.close()
        if not self.output.closed:
            self.output.close()

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done, to make
        sure it's okay. Expect a yes/no answer to `prompt' which is printed,
        suffixed with a question mark and the default value.  The user
        response converted to a boolean is returned."""
        if default:
            prompt += '? (Y or n) '
        else:
            prompt += '? (N or y) '
        while True:
            try:
                reply = self.readline(prompt)
                reply = reply.strip().lower()
            except EOFError:
                return default

            if reply in ('y', 'yes'):
                return True
            elif reply in ('n', 'no'):
                return False
            else:
                self.msg('Please answer y or n.')

        return default

    def errmsg(self, msg, prefix='** '):
        """Common routine for reporting debugger error messages.
        """
        return self.msg('%s%s' % (prefix, msg))

    def finalize(self, last_wishes=None):
        try:
            self.msg("trepan2: That's all, folks...")
            self.close()
        except IOError:
            pass

    def read_command(self, prompt=''):
        line = self.readline(prompt)
        return line

    def readline(self, prompt=''):
        if hasattr(self.input, 'use_raw') and not self.input.use_raw and prompt and len(prompt) > 0:
            self.output.write(prompt)
            self.output.flush()
        return self.input.readline(prompt=prompt)


if __name__ == '__main__':
    intf = UserInterface()
    intf.errmsg('Houston, we have a problem here!')
    import sys
    if len(sys.argv) > 1:
        try:
            line = intf.readline('Type something: ')
        except EOFError:
            print 'No input EOF: '
        else:
            print 'You typed: %s' % line

        line = intf.confirm('Are you sure', False)
        print 'You typed: %s' % line
        line = intf.confirm('Are you not sure', True)
        print 'You typed: %s' % line