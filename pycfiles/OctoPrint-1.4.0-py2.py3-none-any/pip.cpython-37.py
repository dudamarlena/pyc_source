# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Devel\OctoPrint\OctoPrint\src\octoprint\plugins\softwareupdate\updaters\pip.py
# Compiled at: 2020-02-26 04:08:42
# Size of source mod 2**32: 5317 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
__author__ = 'Gina Häußge <osd@foosel.net>'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = 'Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License'
import logging, pkg_resources
from octoprint.util.pip import PipCaller, UnknownPip
from octoprint.util.version import get_comparable_version
from .. import exceptions
logger = logging.getLogger('octoprint.plugins.softwareupdate.updaters.pip')
console_logger = logging.getLogger('octoprint.plugins.softwareupdate.updaters.pip.console')
_ALREADY_INSTALLED = 'Requirement already satisfied (use --upgrade to upgrade)'
_POTENTIAL_EGG_PROBLEM_POSIX = 'No such file or directory'
_POTENTIAL_EGG_PROBLEM_WINDOWS = 'The system cannot find the file specified'
_pip_callers = dict()
_pip_version_dependency_links = pkg_resources.parse_version('1.5')

def can_perform_update(target, check, online=True):
    from .. import MINIMUM_PIP
    pip_caller = _get_pip_caller(command=(check['pip_command'] if 'pip_command' in check else None))
    return 'pip' in check and pip_caller is not None and pip_caller.available and pip_caller.version >= get_comparable_version(MINIMUM_PIP) and (online or check.get('offline', False))


def _get_pip_caller(command=None):
    key = command
    if command is None:
        key = '__default'
    if key not in _pip_callers:
        try:
            _pip_callers[key] = PipCaller(configured=command)
        except UnknownPip:
            _pip_callers[key] = None

    return _pip_callers[key]


def perform_update(target, check, target_version, log_cb=None, online=True, force=False):
    pip_command = None
    if 'pip_command' in check:
        pip_command = check['pip_command']
    pip_working_directory = None
    if 'pip_cwd' in check:
        pip_working_directory = check['pip_cwd']
    if not online:
        if not check.get('offline', False):
            raise exceptions.CannotUpdateOffline()
    pip_caller = _get_pip_caller(command=pip_command)
    if pip_caller is None:
        raise exceptions.UpdateError("Can't run pip", None)
    else:

        def _log_call(*lines):
            _log(lines, prefix=' ', stream='call')

        def _log_stdout(*lines):
            _log(lines, prefix='>', stream='stdout')

        def _log_stderr(*lines):
            _log(lines, prefix='!', stream='stderr')

        def _log_message(*lines):
            _log(lines, prefix='#', stream='message')

        def _log(lines, prefix=None, stream=None):
            if log_cb is None:
                return
            log_cb(lines, prefix=prefix, stream=stream)

        if log_cb is not None:
            pip_caller.on_log_call = _log_call
            pip_caller.on_log_stdout = _log_stdout
            pip_caller.on_log_stderr = _log_stderr
        install_arg = check['pip'].format(target_version=target_version, target=target_version)
        logger.debug('Target: %s, executing pip install %s' % (target, install_arg))
        pip_args = ['--disable-pip-version-check', 'install', install_arg, '--no-cache-dir']
        pip_kwargs = dict(env=dict(PYTHONWARNINGS=b'ignore:DEPRECATION::pip._internal.cli.base_command'))
        if pip_working_directory is not None:
            pip_kwargs.update(cwd=pip_working_directory)
        if 'dependency_links' in check:
            if check['dependency_links']:
                pip_args += ['--process-dependency-links']
        returncode, stdout, stderr = (pip_caller.execute)(*pip_args, **pip_kwargs)
        if returncode != 0:

            def is_egg_problem--- This code section failed: ---

 L. 106         0  LOAD_GLOBAL              _POTENTIAL_EGG_PROBLEM_POSIX
                2  LOAD_FAST                'line'
                4  COMPARE_OP               in
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_GLOBAL              _POTENTIAL_EGG_PROBLEM_WINDOWS
               10  LOAD_FAST                'line'
               12  COMPARE_OP               in
               14  JUMP_IF_FALSE_OR_POP    22  'to 22'
             16_0  COME_FROM             6  '6'
               16  LOAD_STR                 '.egg'
               18  LOAD_FAST                'line'
               20  COMPARE_OP               in
             22_0  COME_FROM            14  '14'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

            if any(map(lambda x: is_egg_problem(x), stderr)) or any(map(lambda x: is_egg_problem(x), stdout)):
                _log_message('This looks like an error caused by a specific issue in upgrading Python "eggs"', 'via current versions of pip.', 'Performing a second install attempt as a work around.')
                returncode, stdout, stderr = (pip_caller.execute)(*pip_args, **pip_kwargs)
                if returncode != 0:
                    raise exceptions.UpdateError('Error while executing pip install', (stdout, stderr))
            else:
                raise exceptions.UpdateError('Error while executing pip install', (stdout, stderr))
    if not force:
        if any(map(lambda x: x.strip().startswith(_ALREADY_INSTALLED) and (install_arg in x or install_arg in x.lower()), stdout)):
            _log_message('Looks like we were already installed in this version. Forcing a reinstall.')
            force = True
    if force:
        logger.debug('Target: %s, executing pip install %s --ignore-reinstalled --force-reinstall --no-deps' % (target, install_arg))
        pip_args += ['--ignore-installed', '--force-reinstall', '--no-deps']
        returncode, stdout, stderr = (pip_caller.execute)(*pip_args, **pip_kwargs)
        if returncode != 0:
            raise exceptions.UpdateError('Error while executing pip install --force-reinstall', (stdout, stderr))
    return 'ok'