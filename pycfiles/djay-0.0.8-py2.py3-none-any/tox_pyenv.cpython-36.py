# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/tox-pyenv/tox_pyenv.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 4407 bytes
"""tox-pyenv

Plugin for the tox_get_python_executable using tox's plugin system:

    https://testrun.org/tox/latest/plugins.html#tox.hookspecs.tox_get_python_executable

Modified to instead use `pyenv which` to locate the
appropriate python executable. This takes the place
of the standard behavior in tox. The built-in default
for the tox_get_python_exeucutable function
is the following (for sys.platform != 'win32'):

    @hookimpl
    def tox_get_python_executable(envconfig):
        return py.path.local.sysfind(envconfig.basepython)

which uses the 'py' package's sysfind():

    https://pylib.readthedocs.org/en/latest/path.html#py._path.local.LocalPath.sysfind

If `pyenv`'s shims are not at the very front of your path,
sysfind might lookup the global system version of python
instead of preferring a version specified by using `pyenv local`
or `pyenv global`. This plugin changes the way tox finds
your python executable to exclusively use `pyenv which`.

    https://github.com/yyuu/pyenv/blob/master/COMMANDS.md#pyenv-which

"""
__title__ = 'tox-pyenv'
__summary__ = 'tox plugin that makes tox use `pyenv which` to find python executables'
__url__ = 'https://github.com/samstav/tox-pyenv'
__version__ = '1.0.2'
__author__ = 'Sam Stavinoha'
__email__ = 'smlstvnh@gmail.com'
__keywords__ = ['tox', 'pyenv', 'python']
__license__ = 'Apache License, Version 2.0'
import logging, subprocess, py
from tox import hookimpl as tox_hookimpl
LOG = logging.getLogger(__name__)

class ToxPyenvException(Exception):
    __doc__ = 'Base class for exceptions from this plugin.'


class PyenvMissing(ToxPyenvException, RuntimeError):
    __doc__ = 'The pyenv program is not installed.'


class PyenvWhichFailed(ToxPyenvException):
    __doc__ = 'Calling `pyenv which` failed.'


@tox_hookimpl
def tox_get_python_executable(envconfig):
    try:
        pyenv = getattr(py.path.local.sysfind('pyenv'), 'strpath', 'pyenv') or 'pyenv'
        cmd = [pyenv, 'which', envconfig.basepython]
        pipe = subprocess.Popen(cmd,
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE),
          universal_newlines=True)
        out, err = pipe.communicate()
    except OSError:
        raise PyenvMissing("pyenv doesn't seem to be installed, you probably don't want this plugin installed either.")

    if pipe.poll() == 0:
        return out.strip()
    if not envconfig.tox_pyenv_fallback:
        raise PyenvWhichFailed(err)
    LOG.debug('`%s` failed thru tox-pyenv plugin, falling back. STDERR: "%s" | To disable this behavior, set tox_pyenv_fallback=False in your tox.ini or use  --tox-pyenv-no-fallback on the command line.', ' '.join([str(x) for x in cmd]), err)


def _setup_no_fallback(parser):
    """Add the option, --tox-pyenv-no-fallback.

    If this option is set, do not allow fallback to tox's built-in
    strategy for looking up python executables if the call to `pyenv which`
    by this plugin fails. This will allow the error to raise instead
    of falling back to tox's default behavior.
    """
    cli_dest = 'tox_pyenv_fallback'
    halp = "If `pyenv which {basepython}` exits non-zero when looking up the python executable, do not allow fallback to tox's built-in default logic."
    tox_pyenv_group = parser.argparser.add_argument_group(title=('{} plugin options'.format(__title__)))
    tox_pyenv_group.add_argument('--tox-pyenv-no-fallback',
      '-F', dest=cli_dest,
      default=True,
      action='store_false',
      help=halp)

    def _pyenv_fallback(testenv_config, value):
        cli_says = getattr(testenv_config.config.option, cli_dest)
        return cli_says or value

    parser.add_testenv_attribute(name=cli_dest,
      type='bool',
      postprocess=_pyenv_fallback,
      default=False,
      help="If `pyenv which {basepython}` exits non-zero when looking up the python executable, allow fallback to tox's built-in default logic.")


@tox_hookimpl
def tox_addoption(parser):
    _setup_no_fallback(parser)