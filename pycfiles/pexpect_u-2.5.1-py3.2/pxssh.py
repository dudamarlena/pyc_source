# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/pxssh.py
# Compiled at: 2011-11-02 15:34:07
"""This class extends pexpect.spawn to specialize setting up SSH connections.
This adds methods for login, logout, and expecting the shell prompt.

$Id: pxssh.py 523 2010-10-17 11:01:22Z noah $
"""
from pexpect import *
import pexpect, time, os
__all__ = [
 'ExceptionPxssh', 'pxssh']

class ExceptionPxssh(ExceptionPexpect):
    """Raised for pxssh exceptions.
    """
    pass


class pxssh(spawn):
    """This class extends pexpect.spawn to specialize setting up SSH
    connections. This adds methods for login, logout, and expecting the shell
    prompt. It does various tricky things to handle many situations in the SSH
    login process. For example, if the session is your first login, then pxssh
    automatically accepts the remote certificate; or if you have public key
    authentication setup then pxssh won't wait for the password prompt.

    pxssh uses the shell prompt to synchronize output from the remote host. In
    order to make this more robust it sets the shell prompt to something more
    unique than just $ or #. This should work on most Borne/Bash or Csh style
    shells.

    Example that runs a few commands on a remote server and prints the result::

        import pxssh
        import getpass
        try:
            s = pxssh.pxssh()
            hostname = raw_input('hostname: ')
            username = raw_input('username: ')
            password = getpass.getpass('password: ')
            s.login (hostname, username, password)
            s.sendline ('uptime')  # run a command
            s.prompt()             # match the prompt
            print s.before         # print everything before the prompt.
            s.sendline ('ls -l')
            s.prompt()
            print s.before
            s.sendline ('df')
            s.prompt()
            print s.before
            s.logout()
        except pxssh.ExceptionPxssh, e:
            print "pxssh failed on login."
            print str(e)

    Note that if you have ssh-agent running while doing development with pxssh
    then this can lead to a lot of confusion. Many X display managers (xdm,
    gdm, kdm, etc.) will automatically start a GUI agent. You may see a GUI
    dialog box popup asking for a password during development. You should turn
    off any key agents during testing. The 'force_password' attribute will turn
    off public key authentication. This will only work if the remote SSH server
    is configured to allow password logins. Example of using 'force_password'
    attribute::

            s = pxssh.pxssh()
            s.force_password = True
            hostname = raw_input('hostname: ')
            username = raw_input('username: ')
            password = getpass.getpass('password: ')
            s.login (hostname, username, password)
    """

    def __init__(self, timeout=30, maxread=2000, searchwindowsize=None, logfile=None, cwd=None, env=None):
        spawn.__init__(self, None, timeout=timeout, maxread=maxread, searchwindowsize=searchwindowsize, logfile=logfile, cwd=cwd, env=env)
        self.name = '<pxssh>'
        self.UNIQUE_PROMPT = '\\[PEXPECT\\][\\$\\#] '
        self.PROMPT = self.UNIQUE_PROMPT
        self.PROMPT_SET_SH = "PS1='[PEXPECT]\\$ '"
        self.PROMPT_SET_CSH = "set prompt='[PEXPECT]\\$ '"
        self.SSH_OPTS = "-o'RSAAuthentication=no' -o 'PubkeyAuthentication=no'"
        self.force_password = False
        self.auto_prompt_reset = True
        return

    def levenshtein_distance(self, a, b):
        """This calculates the Levenshtein distance between a and b.
        """
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n
        current = list(range(n + 1))
        for i in range(1, m + 1):
            previous, current = current, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete = previous[j] + 1, current[(j - 1)] + 1
                change = previous[(j - 1)]
                if a[(j - 1)] != b[(i - 1)]:
                    change = change + 1
                current[j] = min(add, delete, change)

        return current[n]

    def sync_original_prompt(self):
        """This attempts to find the prompt. Basically, press enter and record
        the response; press enter again and record the response; if the two
        responses are similar then assume we are at the original prompt. This
        is a slow function. It can take over 10 seconds. """
        self.sendline()
        time.sleep(0.1)
        try:
            self.read_nonblocking(size=10000, timeout=1)
        except TIMEOUT:
            pass

        time.sleep(0.1)
        self.sendline()
        time.sleep(0.5)
        x = self.read_nonblocking(size=1000, timeout=1)
        time.sleep(0.1)
        self.sendline()
        time.sleep(0.5)
        a = self.read_nonblocking(size=1000, timeout=1)
        time.sleep(0.1)
        self.sendline()
        time.sleep(0.5)
        b = self.read_nonblocking(size=1000, timeout=1)
        ld = self.levenshtein_distance(a, b)
        len_a = len(a)
        if len_a == 0:
            return False
        if float(ld) / len_a < 0.4:
            return True
        return False

    def login(self, server, username, password='', terminal_type='ansi', original_prompt='[#$]', login_timeout=10, port=None, auto_prompt_reset=True, ssh_key=None):
        """This logs the user into the given server. It uses the
        'original_prompt' to try to find the prompt right after login. When it
        finds the prompt it immediately tries to reset the prompt to something
        more easily matched. The default 'original_prompt' is very optimistic
        and is easily fooled. It's more reliable to try to match the original
        prompt as exactly as possible to prevent false matches by server
        strings such as the "Message Of The Day". On many systems you can
        disable the MOTD on the remote server by creating a zero-length file
        called "~/.hushlogin" on the remote server. If a prompt cannot be found
        then this will not necessarily cause the login to fail. In the case of
        a timeout when looking for the prompt we assume that the original
        prompt was so weird that we could not match it, so we use a few tricks
        to guess when we have reached the prompt. Then we hope for the best and
        blindly try to reset the prompt to something more unique. If that fails
        then login() raises an ExceptionPxssh exception.

        In some situations it is not possible or desirable to reset the
        original prompt. In this case, set 'auto_prompt_reset' to False to
        inhibit setting the prompt to the UNIQUE_PROMPT. Remember that pxssh
        uses a unique prompt in the prompt() method. If the original prompt is
        not reset then this will disable the prompt() method unless you
        manually set the PROMPT attribute. """
        ssh_options = '-q'
        if self.force_password:
            ssh_options = ssh_options + ' ' + self.SSH_OPTS
        if port is not None:
            ssh_options = ssh_options + ' -p %s' % str(port)
        if ssh_key is not None:
            try:
                os.path.isfile(ssh_key)
            except:
                raise ExceptionPxssh('private ssh key does not exist')

            ssh_options = ssh_options + ' -i %s' % ssh_key
        cmd = 'ssh %s -l %s %s' % (ssh_options, username, server)
        spawn._spawn(self, cmd)
        i = self.expect(['(?i)are you sure you want to continue connecting', original_prompt, '(?i)(?:password)|(?:passphrase for key)', '(?i)permission denied', '(?i)terminal type', TIMEOUT, '(?i)connection closed by remote host'], timeout=login_timeout)
        if i == 0:
            self.sendline('yes')
            i = self.expect(['(?i)are you sure you want to continue connecting', original_prompt, '(?i)(?:password)|(?:passphrase for key)', '(?i)permission denied', '(?i)terminal type', TIMEOUT])
        if i == 2:
            self.sendline(password)
            i = self.expect(['(?i)are you sure you want to continue connecting', original_prompt, '(?i)(?:password)|(?:passphrase for key)', '(?i)permission denied', '(?i)terminal type', TIMEOUT])
        if i == 4:
            self.sendline(terminal_type)
            i = self.expect(['(?i)are you sure you want to continue connecting', original_prompt, '(?i)(?:password)|(?:passphrase for key)', '(?i)permission denied', '(?i)terminal type', TIMEOUT])
        if i == 0:
            self.close()
            raise ExceptionPxssh('Weird error. Got "are you sure" prompt twice.')
        else:
            if i == 1:
                pass
            else:
                if i == 2:
                    self.close()
                    raise ExceptionPxssh('password refused')
                else:
                    if i == 3:
                        self.close()
                        raise ExceptionPxssh('permission denied')
                    else:
                        if i == 4:
                            self.close()
                            raise ExceptionPxssh('Weird error. Got "terminal type" prompt twice.')
                        else:
                            if i == 5:
                                pass
                            else:
                                if i == 6:
                                    self.close()
                                    raise ExceptionPxssh('connection closed')
                                else:
                                    self.close()
                                    raise ExceptionPxssh('unexpected login response')
        if not self.sync_original_prompt():
            self.close()
            raise ExceptionPxssh('could not synchronize with original prompt')
        if auto_prompt_reset:
            if not self.set_unique_prompt():
                self.close()
                raise ExceptionPxssh('could not set shell prompt\n' + self.before)
        return True

    def logout(self):
        """This sends exit to the remote shell. If there are stopped jobs then
        this automatically sends exit twice. """
        self.sendline('exit')
        index = self.expect([EOF, '(?i)there are stopped jobs'])
        if index == 1:
            self.sendline('exit')
            self.expect(EOF)
        self.close()

    def prompt(self, timeout=-1):
        """This matches the shell prompt. This is little more than a short-cut
        to the expect() method. This returns True if the shell prompt was
        matched. This returns False if a timeout was raised. Note that if you
        called login() with auto_prompt_reset set to False then before calling
        prompt() you must set the PROMPT attribute to a regex that prompt()
        will use for matching the prompt. Calling prompt() will erase the
        contents of the 'before' attribute even if no prompt is ever matched.
        If timeout is not given or it is set to -1 then self.timeout is used.
        """
        if timeout == -1:
            timeout = self.timeout
        i = self.expect([self.PROMPT, TIMEOUT], timeout=timeout)
        if i == 1:
            return False
        return True

    def set_unique_prompt(self):
        """This sets the remote prompt to something more unique than # or $.
        This makes it easier for the prompt() method to match the shell prompt
        unambiguously. This method is called automatically by the login()
        method, but you may want to call it manually if you somehow reset the
        shell prompt. For example, if you 'su' to a different user then you
        will need to manually reset the prompt. This sends shell commands to
        the remote host to set the prompt, so this assumes the remote host is
        ready to receive commands.

        Alternatively, you may use your own prompt pattern. Just set the PROMPT
        attribute to a regular expression that matches it. In this case you
        should call login() with auto_prompt_reset=False; then set the PROMPT
        attribute. After that the prompt() method will try to match your prompt
        pattern."""
        self.sendline('unset PROMPT_COMMAND')
        self.sendline(self.PROMPT_SET_SH)
        i = self.expect([TIMEOUT, self.PROMPT], timeout=10)
        if i == 0:
            self.sendline(self.PROMPT_SET_CSH)
            i = self.expect([TIMEOUT, self.PROMPT], timeout=10)
            if i == 0:
                return False
        return True