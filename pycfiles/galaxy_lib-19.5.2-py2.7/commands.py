# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/commands.py
# Compiled at: 2018-04-20 03:19:42
"""Generic I/O and shell processing code used by Galaxy tool dependencies."""
import logging, os, subprocess, sys as _sys, six
from six.moves import shlex_quote
from galaxy.util import unicodify, which
log = logging.getLogger(__name__)
STDOUT_INDICATOR = '-'

def redirecting_io(sys=_sys):
    """Predicate to determine if we are redicting stdout in process."""
    assert sys is not None
    try:
        sys.stdout.fileno()
    except Exception:
        return True

    return False
    return


def redirect_aware_commmunicate(p, sys=_sys):
    """Variant of process.communicate that works with in process I/O redirection."""
    if not sys is not None:
        raise AssertionError
        out, err = p.communicate()
        if redirecting_io(sys=sys):
            if out:
                if not six.PY2:
                    out = unicodify(out)
                sys.stdout.write(out)
                out = None
            if err:
                err = six.PY2 or unicodify(err)
            sys.stderr.write(err)
            err = None
    return (
     out, err)


def shell(cmds, env=None, **kwds):
    """Run shell commands with `shell_process` and wait."""
    sys = kwds.get('sys', _sys)
    assert sys is not None
    p = shell_process(cmds, env, **kwds)
    if redirecting_io(sys=sys):
        redirect_aware_commmunicate(p, sys=sys)
        exit = p.returncode
        return exit
    else:
        return p.wait()
        return


def shell_process(cmds, env=None, **kwds):
    """A high-level method wrapping subprocess.Popen.

    Handles details such as environment extension and in process I/O
    redirection.
    """
    sys = kwds.get('sys', _sys)
    popen_kwds = dict()
    if isinstance(cmds, six.string_types):
        log.warning('Passing program arguments as a string may be a security hazard if combined with untrusted input')
        popen_kwds['shell'] = True
    if kwds.get('stdout', None) is None and redirecting_io(sys=sys):
        popen_kwds['stdout'] = subprocess.PIPE
    if kwds.get('stderr', None) is None and redirecting_io(sys=sys):
        popen_kwds['stderr'] = subprocess.PIPE
    popen_kwds.update(**kwds)
    if env:
        new_env = os.environ.copy()
        new_env.update(env)
        popen_kwds['env'] = new_env
    p = subprocess.Popen(cmds, **popen_kwds)
    return p


def execute(cmds):
    """Execute commands and throw an exception on a non-zero exit.

    Return the standard output if the commands are successful
    """
    return _wait(cmds, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def argv_to_str(command_argv, quote=True):
    """Convert an argv command list to a string for shell subprocess.

    If None appears in the command list it is simply excluded.

    Arguments are quoted with shlex_quote. That said, this method is not meant to be
    used in security critical paths of code and should not be used to sanitize
    code.
    """
    map_func = shlex_quote if quote else (lambda x: x)
    return (' ').join([ map_func(c) for c in command_argv if c is not None ])


def _wait(cmds, **popen_kwds):
    p = subprocess.Popen(cmds, **popen_kwds)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise CommandLineException(argv_to_str(cmds), stdout, stderr, p.returncode)
    return stdout


def download_command(url, to=STDOUT_INDICATOR, quote_url=False):
    """Build a command line to download a URL.

    By default the URL will be downloaded to standard output but a specific
    file can be specified with the `to` argument.
    """
    if quote_url:
        url = "'%s'" % url
        if to != STDOUT_INDICATOR:
            to = "'%s'" % to
    if which('wget'):
        download_cmd = [
         'wget', '-q']
        if to == STDOUT_INDICATOR:
            download_cmd.extend(['-O', STDOUT_INDICATOR, url])
        else:
            download_cmd.extend(['--recursive', '-O', to, url])
    else:
        download_cmd = [
         'curl', '-L', url]
        if to != STDOUT_INDICATOR:
            download_cmd.extend(['-o', to])
    return download_cmd


class CommandLineException(Exception):
    """An exception indicating a non-zero command-line exit."""

    def __init__(self, command, stdout, stderr, returncode):
        """Construct a CommandLineException from command and standard I/O."""
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.message = 'Failed to execute command-line %s, stderr was:\n-------->>begin stderr<<--------\n%s\n-------->>end stderr<<--------\n-------->>begin stdout<<--------\n%s\n-------->>end stdout<<--------\n' % (
         command, stderr, stdout)

    def __str__(self):
        """Return a verbose error message indicating the command problem."""
        return self.message


__all__ = ('argv_to_str', 'CommandLineException', 'download_command', 'execute', 'redirect_aware_commmunicate',
           'redirecting_io', 'shell', 'shell_process', 'which')