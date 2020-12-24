# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/subproc.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 8757 bytes
"""Safely invoke external binaries."""
import logging, os, subprocess, yaml, treadmill
_LOGGER = logging.getLogger(__name__)
EXECUTABLES = None
_CLOSE_FDS = os.name != 'nt'

class CommandWhitelistError(Exception):
    __doc__ = 'Error if not in whitelist.'


def _load():
    """Load whitelist of external binaries that can invoked."""
    global EXECUTABLES
    bin_whitelists = os.environ.get('TREADMILL_EXE_WHITELIST')
    assert bin_whitelists is not None
    _LOGGER.debug('Loading whitelist: %s', bin_whitelists)
    exes = {}
    for bin_whitelist in bin_whitelists.split(':'):
        _LOGGER.debug('Loading whitelist: %s', bin_whitelist)
        with open(bin_whitelist) as (f):
            exes.update(yaml.load(f.read()))

    EXECUTABLES = exes


def _check(path):
    """Check that path exists and is executable."""
    if path is None:
        return False
    else:
        if path.endswith('.so') and (path.find('$ISA') >= 0 or path.find('$LIB') >= 0):
            return True
        return os.access(path, os.X_OK)


def resolve(exe):
    """Resolve logical name to full path."""
    if exe.startswith(treadmill.TREADMILL):
        return exe
    if EXECUTABLES is None:
        _load()
    if exe not in EXECUTABLES:
        _LOGGER.critical('Not in whitelist: %s', exe)
        raise CommandWhitelistError()
    safe_exe = EXECUTABLES[exe]
    if isinstance(safe_exe, list):
        for choice in safe_exe:
            if _check(choice):
                return choice

        _LOGGER.critical('Cannot resolve: %s', exe)
        raise CommandWhitelistError()
    elif not _check(safe_exe):
        print('Not found: ', exe, safe_exe)
        _LOGGER.critical('Command not found: %s, %s', exe, safe_exe)
        raise CommandWhitelistError()
    return safe_exe


def _whitelist_command(cmdline):
    """Checks that the command line is in the whitelist."""
    safe_cmdline = list(cmdline)
    safe_cmdline.insert(0, resolve(safe_cmdline.pop(0)))
    return safe_cmdline


def check_call(cmdline, environ=(), runas=None, **kwargs):
    """Runs command wrapping subprocess.check_call.

    :param cmdline:
        Command to run
    :type cmdline:
        ``list``
    :param environ:
        *optional* Environ variable to set prior to running the command
    :type environ:
        ``dict``
    :param runas:
        *optional* Run as user.
    :type runas:
        ``str``
    """
    _LOGGER.debug('check_call environ: %r, runas: %r, %r', environ, runas, cmdline)
    args = _whitelist_command(cmdline)
    if runas:
        s6_setguid = os.path.join(resolve('s6'), 'bin', 's6-setuidgid')
        args = [s6_setguid, runas] + args
    cmd_environ = dict(os.environ.items())
    cmd_environ.update(environ)
    try:
        rc = subprocess.check_call(args, close_fds=_CLOSE_FDS, env=cmd_environ, **kwargs)
        _LOGGER.debug('Finished, rc: %d', rc)
        return rc
    except subprocess.CalledProcessError as exc:
        _LOGGER.warn(exc.output)
        raise


def check_output(cmdline, environ=(), **kwargs):
    """Runs command wrapping subprocess.check_output.

    :param cmdline:
        Command to run
    :type cmdline:
        ``list``
    :param environ:
        *optional* Environ variable to set prior to running the command
    :type environ:
        ``dict``
    """
    _LOGGER.debug('check_output environ: %r, %r', environ, cmdline)
    args = _whitelist_command(cmdline)
    cmd_environ = dict(os.environ.items())
    cmd_environ.update(environ)
    try:
        res = subprocess.check_output(args, close_fds=_CLOSE_FDS, env=cmd_environ, **kwargs)
        _LOGGER.debug('Finished.')
    except subprocess.CalledProcessError as exc:
        _LOGGER.warn(exc.output)
        raise

    return res.decode()


def call(cmdline, environ=(), **kwargs):
    """Runs command wrapping subprocess.call.

    :param cmdline:
        Command to run
    :type cmdline:
        ``list``
    :param environ:
        *optional* Environ variable to set prior to running the command
    :type environ:
        ``dict``
    """
    _LOGGER.debug('run: %r', cmdline)
    args = _whitelist_command(cmdline)
    cmd_environ = dict(os.environ.items())
    cmd_environ.update(environ)
    rc = subprocess.call(args, close_fds=_CLOSE_FDS, env=cmd_environ, **kwargs)
    _LOGGER.debug('Finished, rc: %d', rc)
    return rc


def invoke(cmd, cmd_input=None, use_except=False, **environ):
    """Runs command and return return code and output.

    Allows passing some input and/or setting all keyword arguments as environ
    variables.

    :param cmd:
        Command to run
    :type cmd:
        ``list``
    :param cmd_input:
        *optional* Provide some input to be passed to the command's STDIN
    :type cmd_input:
        ``str``
    :param environ:
        Environ variable to set prior to running the command
    :type environ:
        ``dict``
    :returns:
        (``(int, str)``) -- Return code and output from executed process
    :raises:
        :class:`subprocess.CalledProcessError`
    """
    _LOGGER.debug('invoke: %r', cmd)
    args = _whitelist_command(cmd)
    cmd_environ = dict(os.environ.items())
    cmd_environ.update(**environ)
    try:
        proc = subprocess.Popen(args, close_fds=_CLOSE_FDS, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=cmd_environ)
        out, _err = proc.communicate(cmd_input)
        retcode = proc.returncode
    except Exception:
        _LOGGER.exception('Error invoking %r', args)
        raise

    if retcode != 0:
        if use_except:
            raise subprocess.CalledProcessError(cmd=args, returncode=retcode, output=out)
    return (
     retcode, out)


def invoke_return(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **environ):
    """Runs command and return, let caller handle process

    Allows passing some input and/or setting all keyword arguments as environ
    variables.

    :param cmd: Command to run
    :type cmd: ``list``

    :param stdin:
        *optional* Provide PIPE for stdin; default is subprocess.PIPE
    :type stdin: ``PIPE``
    :param stdout:
        *optional* Provide PIPE for stdout; default is subprocess.PIPE
    :type stdout: ``PIPE``

    :param stderr:
        *optional* Provide PIPE for stderr; default is subprocess.STSOUT
    :type stderr: ``PIPE``

    :param environ:
        Environ variable to set prior to running the command
    :type environ: ``dict``

    :returns:
        :class:`subprocess.Proc`
    :raises:
        :class:`subprocess.CalledProcessError`
    """
    _LOGGER.debug('invoke: %r', cmd)
    args = _whitelist_command(cmd)
    cmd_environ = dict(os.environ.items())
    cmd_environ.update(**environ)
    try:
        return subprocess.Popen(args, close_fds=_CLOSE_FDS, shell=False, stdin=stdin, stdout=stdout, stderr=stderr, env=cmd_environ)
    except Exception:
        _LOGGER.exception('Error invoking %r', args)
        raise


def exec_pid1(cmd, ipc=True, mount=True, proc=True):
    """Exec command line under pid1."""
    pid1 = resolve('pid1')
    safe_cmd = _whitelist_command(cmd)
    args = [pid1]
    if ipc:
        args.append('-i')
    if mount:
        args.append('-m')
    if proc:
        args.append('-p')
    args.extend(safe_cmd)
    _LOGGER.debug('exec_pid1: %r', args)
    os.execvp(args[0], args)


def safe_exec(cmd):
    """Exec command line using os.execvp."""
    safe_cmd = _whitelist_command(cmd)
    _LOGGER.debug('safe_cmd: %r', safe_cmd)
    os.execvp(safe_cmd[0], safe_cmd)