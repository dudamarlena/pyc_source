# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hpssa/_cli.py
# Compiled at: 2018-10-02 22:16:08
import logging, os, shlex, subprocess
log = logging.getLogger(__name__)

class CLIResult(str):
    ENCODING = 'utf-8'

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, object=cls.__decode(args[0]))

    def __init__(self, stdout='', stderr='', returncode=None):
        """Constructs a new CLIResult containing a command result."""
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode
        super(CLIResult, self).__init__()

    @classmethod
    def __decode(cls, v):
        if isinstance(v, bytes):
            return v.decode(cls.ENCODING)
        return v

    def __str__(self):
        return self.__decode(self._stdout)

    def __repr__(self):
        return self.__str__()

    @property
    def stdout(self):
        return self.__str__()

    @property
    def stderr(self):
        return self.__decode(self._stderr)

    @stdout.setter
    def stdout(self, value):
        self._stdout = value

    @stderr.setter
    def stderr(self, value):
        self._stderr = value


class CLIException(Exception):
    """Exception used by cli.run function."""
    pass


def run(command, bufsize=1048567, dry_run=False, raise_exception=False, ignore_error=False, quiet=False, env=None, _input=None):
    """Runs a command and returns its result.

    The command result (stdout, stderr, and return code) is stored
    in a CLIResult instance.

    :param command: Command to execute.
    :type command: str.
    :param bufsize: Buffer line size.
    :type bufsize: int.
    :param dry_run: Should we perform a dry run of the command.
    :type dry_run: bool.
    :param raise_exception: Boolean indicating whether to raise an exception
        when an error occurs.
    :param ignore_error: Boolean indicating if errors should be ignored.
    :param env: Dict containing variables to add to the environment.
    :param quiet: Boolean indicating if debug logs should be silenced.
    :param _input: Pass data into stdin fd

    :returns: :func:`mercury_CLIResult`.
    """
    if not quiet:
        log.debug(('Running: {}').format(command))
    our_env = os.environ.copy()
    our_env.update(env or dict())
    cmd = shlex.split(str(command))
    stdin = _input and subprocess.PIPE or None
    if not dry_run:
        try:
            p = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=bufsize, env=our_env)
            out, err = p.communicate(input=_input)
            ret = p.returncode
        except (OSError, ValueError) as e:
            error = ("Failed while executing '{}': {}").format((' ').join(cmd), e)
            log.error(error)
            if raise_exception:
                raise CLIException(error)
            return CLIResult('', error, 1)

    else:
        out, err, ret = ('', '', 0)
    if not quiet:
        log.debug(('Return Code: {}').format(ret))
        if out:
            log.debug(('stdout: \n{}').format(out.strip()))
    if ret and not ignore_error:
        log.error(('Return: {} running: {} stdout: {}\nstderr: \n{}').format(ret, command, out.strip(), err.strip()))
        if raise_exception:
            raise CLIException(err)
    cli_result = CLIResult(out, err, ret)
    return cli_result


def find_in_path(filename):
    """Find a file by its absolute path or in $PATH.

    :param filename: The name of the file to find. If filename is an absolute
        path, this will check the file exists. Otherwise, this will look for
        the file in $PATH.
    :returns: The absolute path of the file if it's found, None if not found.
    """
    if os.path.split(filename)[0]:
        _temp_path = os.path.realpath(os.path.expanduser(filename))
        if os.path.exists(_temp_path):
            return _temp_path
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            abspath = os.path.join(path, filename)
            if os.path.exists(abspath):
                return abspath