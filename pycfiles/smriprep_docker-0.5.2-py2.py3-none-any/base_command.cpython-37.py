# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/cli/base_command.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 7948 bytes
"""Base Command class, and related routines"""
from __future__ import absolute_import, print_function
import logging, logging.config, optparse, os, platform, sys, traceback
from pip._internal.cli import cmdoptions
from pip._internal.cli.command_context import CommandContextMixIn
from pip._internal.cli.parser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.cli.status_codes import ERROR, PREVIOUS_BUILD_DIR_ERROR, SUCCESS, UNKNOWN_ERROR, VIRTUALENV_NOT_FOUND
from pip._internal.exceptions import BadCommand, CommandError, InstallationError, PreviousBuildDirError, UninstallationError
from pip._internal.utils.deprecation import deprecated
from pip._internal.utils.filesystem import check_path_owner
from pip._internal.utils.logging import BrokenStdoutLoggingError, setup_logging
from pip._internal.utils.misc import get_prog, normalize_path
from pip._internal.utils.temp_dir import global_tempdir_manager
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.virtualenv import running_under_virtualenv
if MYPY_CHECK_RUNNING:
    from typing import List, Tuple, Any
    from optparse import Values
__all__ = [
 'Command']
logger = logging.getLogger(__name__)

class Command(CommandContextMixIn):
    usage = None
    ignore_require_venv = False

    def __init__(self, name, summary, isolated=False):
        super(Command, self).__init__()
        parser_kw = {'usage':self.usage, 
         'prog':'%s %s' % (get_prog(), name), 
         'formatter':UpdatingDefaultsHelpFormatter(), 
         'add_help_option':False, 
         'name':name, 
         'description':self.__doc__, 
         'isolated':isolated}
        self.name = name
        self.summary = summary
        self.parser = ConfigOptionParser(**parser_kw)
        optgroup_name = '%s Options' % self.name.capitalize()
        self.cmd_opts = optparse.OptionGroup(self.parser, optgroup_name)
        gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, self.parser)
        self.parser.add_option_group(gen_opts)

    def handle_pip_version_check(self, options):
        """
        This is a no-op so that commands by default do not do the pip version
        check.
        """
        assert not hasattr(options, 'no_index')

    def run(self, options, args):
        raise NotImplementedError

    def parse_args(self, args):
        return self.parser.parse_args(args)

    def main(self, args):
        try:
            with self.main_context():
                return self._main(args)
        finally:
            logging.shutdown()

    def _main(self, args):
        self.enter_context(global_tempdir_manager())
        options, args = self.parse_args(args)
        self.verbosity = options.verbose - options.quiet
        level_number = setup_logging(verbosity=(self.verbosity),
          no_color=(options.no_color),
          user_log_file=(options.log))
        if sys.version_info[:2] == (2, 7):
            if not options.no_python_version_warning:
                message = 'A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support'
                if platform.python_implementation() == 'CPython':
                    message = 'Python 2.7 reached the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 is no longer maintained. ' + message
                deprecated(message, replacement=None, gone_in=None)
        if options.skip_requirements_regex:
            deprecated('--skip-requirements-regex is unsupported and will be removed',
              replacement='manage requirements/constraints files explicitly, possibly generating them from metadata',
              gone_in='20.1',
              issue=7297)
        if options.no_input:
            os.environ['PIP_NO_INPUT'] = '1'
        if options.exists_action:
            os.environ['PIP_EXISTS_ACTION'] = ' '.join(options.exists_action)
        if options.require_venv:
            if not self.ignore_require_venv:
                if not running_under_virtualenv():
                    logger.critical('Could not find an activated virtualenv (required).')
                    sys.exit(VIRTUALENV_NOT_FOUND)
        if options.cache_dir:
            options.cache_dir = normalize_path(options.cache_dir)
            if not check_path_owner(options.cache_dir):
                logger.warning("The directory '%s' or its parent directory is not owned or is not writable by the current user. The cache has been disabled. Check the permissions and owner of that directory. If executing pip with sudo, you may want sudo's -H flag.", options.cache_dir)
                options.cache_dir = None
        try:
            try:
                status = self.run(options, args)
                if isinstance(status, int):
                    return status
            except PreviousBuildDirError as exc:
                try:
                    logger.critical(str(exc))
                    logger.debug('Exception information:', exc_info=True)
                    return PREVIOUS_BUILD_DIR_ERROR
                finally:
                    exc = None
                    del exc

            except (InstallationError, UninstallationError, BadCommand) as exc:
                try:
                    logger.critical(str(exc))
                    logger.debug('Exception information:', exc_info=True)
                    return ERROR
                finally:
                    exc = None
                    del exc

            except CommandError as exc:
                try:
                    logger.critical('%s', exc)
                    logger.debug('Exception information:', exc_info=True)
                    return ERROR
                finally:
                    exc = None
                    del exc

            except BrokenStdoutLoggingError:
                print('ERROR: Pipe to stdout was broken', file=(sys.stderr))
                if level_number <= logging.DEBUG:
                    traceback.print_exc(file=(sys.stderr))
                return ERROR
            except KeyboardInterrupt:
                logger.critical('Operation cancelled by user')
                logger.debug('Exception information:', exc_info=True)
                return ERROR
            except BaseException:
                logger.critical('Exception:', exc_info=True)
                return UNKNOWN_ERROR

        finally:
            self.handle_pip_version_check(options)

        return SUCCESS