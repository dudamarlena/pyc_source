# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_internal/cli/base_command.py
# Compiled at: 2019-02-14 00:35:06
"""Base Command class, and related routines"""
from __future__ import absolute_import, print_function
import logging, logging.config, optparse, os, platform, sys, traceback
from pip._internal.cli import cmdoptions
from pip._internal.cli.parser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.cli.status_codes import ERROR, PREVIOUS_BUILD_DIR_ERROR, SUCCESS, UNKNOWN_ERROR, VIRTUALENV_NOT_FOUND
from pip._internal.download import PipSession
from pip._internal.exceptions import BadCommand, CommandError, InstallationError, PreviousBuildDirError, UninstallationError
from pip._internal.index import PackageFinder
from pip._internal.locations import running_under_virtualenv
from pip._internal.req.constructors import install_req_from_editable, install_req_from_line
from pip._internal.req.req_file import parse_requirements
from pip._internal.utils.deprecation import deprecated
from pip._internal.utils.logging import BrokenStdoutLoggingError, setup_logging
from pip._internal.utils.misc import get_prog, normalize_path, redact_password_from_url
from pip._internal.utils.outdated import pip_version_check
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, List, Tuple, Any
    from optparse import Values
    from pip._internal.cache import WheelCache
    from pip._internal.req.req_set import RequirementSet
__all__ = [
 'Command']
logger = logging.getLogger(__name__)

class Command(object):
    name = None
    usage = None
    hidden = False
    ignore_require_venv = False

    def __init__(self, isolated=False):
        parser_kw = {'usage': self.usage, 
           'prog': '%s %s' % (get_prog(), self.name), 
           'formatter': UpdatingDefaultsHelpFormatter(), 
           'add_help_option': False, 
           'name': self.name, 
           'description': self.__doc__, 
           'isolated': isolated}
        self.parser = ConfigOptionParser(**parser_kw)
        optgroup_name = '%s Options' % self.name.capitalize()
        self.cmd_opts = optparse.OptionGroup(self.parser, optgroup_name)
        gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, self.parser)
        self.parser.add_option_group(gen_opts)

    def run(self, options, args):
        raise NotImplementedError

    def _build_session(self, options, retries=None, timeout=None):
        session = PipSession(cache=normalize_path(os.path.join(options.cache_dir, 'http')) if options.cache_dir else None, retries=retries if retries is not None else options.retries, insecure_hosts=options.trusted_hosts)
        if options.cert:
            session.verify = options.cert
        if options.client_cert:
            session.cert = options.client_cert
        if options.timeout or timeout:
            session.timeout = timeout if timeout is not None else options.timeout
        if options.proxy:
            session.proxies = {'http': options.proxy, 'https': options.proxy}
        session.auth.prompting = not options.no_input
        return session

    def parse_args(self, args):
        return self.parser.parse_args(args)

    def main(self, args):
        options, args = self.parse_args(args)
        self.verbosity = options.verbose - options.quiet
        level_number = setup_logging(verbosity=self.verbosity, no_color=options.no_color, user_log_file=options.log)
        if sys.version_info[:2] == (3, 4):
            deprecated("Python 3.4 support has been deprecated. pip 19.1 will be the last one supporting it. Please upgrade your Python as Python 3.4 won't be maintained after March 2019 (cf PEP 429).", replacement=None, gone_in='19.2')
        elif sys.version_info[:2] == (2, 7):
            message = 'A future version of pip will drop support for Python 2.7.'
            if platform.python_implementation() == 'CPython':
                message = "Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. " + message
            deprecated(message, replacement=None, gone_in=None)
        if options.no_input:
            os.environ['PIP_NO_INPUT'] = '1'
        if options.exists_action:
            os.environ['PIP_EXISTS_ACTION'] = (' ').join(options.exists_action)
        if options.require_venv and not self.ignore_require_venv:
            if not running_under_virtualenv():
                logger.critical('Could not find an activated virtualenv (required).')
                sys.exit(VIRTUALENV_NOT_FOUND)
        try:
            try:
                status = self.run(options, args)
                if isinstance(status, int):
                    return status
            except PreviousBuildDirError as exc:
                logger.critical(str(exc))
                logger.debug('Exception information:', exc_info=True)
                return PREVIOUS_BUILD_DIR_ERROR
            except (InstallationError, UninstallationError, BadCommand) as exc:
                logger.critical(str(exc))
                logger.debug('Exception information:', exc_info=True)
                return ERROR
            except CommandError as exc:
                logger.critical('ERROR: %s', exc)
                logger.debug('Exception information:', exc_info=True)
                return ERROR
            except BrokenStdoutLoggingError:
                print('ERROR: Pipe to stdout was broken', file=sys.stderr)
                if level_number <= logging.DEBUG:
                    traceback.print_exc(file=sys.stderr)
                return ERROR
            except KeyboardInterrupt:
                logger.critical('Operation cancelled by user')
                logger.debug('Exception information:', exc_info=True)
                return ERROR
            except BaseException:
                logger.critical('Exception:', exc_info=True)
                return UNKNOWN_ERROR

        finally:
            allow_version_check = hasattr(options, 'no_index') and not (options.disable_pip_version_check or options.no_index)
            if allow_version_check:
                session = self._build_session(options, retries=0, timeout=min(5, options.timeout))
                with session:
                    pip_version_check(session, options)
            logging.shutdown()

        return SUCCESS


class RequirementCommand(Command):

    @staticmethod
    def populate_requirement_set(requirement_set, args, options, finder, session, name, wheel_cache):
        """
        Marshal cmd line args into a requirement set.
        """
        for filename in options.constraints:
            for req_to_add in parse_requirements(filename, constraint=True, finder=finder, options=options, session=session, wheel_cache=wheel_cache):
                req_to_add.is_direct = True
                requirement_set.add_requirement(req_to_add)

        for req in args:
            req_to_add = install_req_from_line(req, None, isolated=options.isolated_mode, use_pep517=options.use_pep517, wheel_cache=wheel_cache)
            req_to_add.is_direct = True
            requirement_set.add_requirement(req_to_add)

        for req in options.editables:
            req_to_add = install_req_from_editable(req, isolated=options.isolated_mode, use_pep517=options.use_pep517, wheel_cache=wheel_cache)
            req_to_add.is_direct = True
            requirement_set.add_requirement(req_to_add)

        for filename in options.requirements:
            for req_to_add in parse_requirements(filename, finder=finder, options=options, session=session, wheel_cache=wheel_cache, use_pep517=options.use_pep517):
                req_to_add.is_direct = True
                requirement_set.add_requirement(req_to_add)

        requirement_set.require_hashes = options.require_hashes
        if not (args or options.editables or options.requirements):
            opts = {'name': name}
            if options.find_links:
                raise CommandError('You must give at least one requirement to %(name)s (maybe you meant "pip %(name)s %(links)s"?)' % dict(opts, links=(' ').join(options.find_links)))
            else:
                raise CommandError('You must give at least one requirement to %(name)s (see "pip help %(name)s")' % opts)
        return

    def _build_package_finder(self, options, session, platform=None, python_versions=None, abi=None, implementation=None):
        """
        Create a package finder appropriate to this requirement command.
        """
        index_urls = [
         options.index_url] + options.extra_index_urls
        if options.no_index:
            logger.debug('Ignoring indexes: %s', (',').join(redact_password_from_url(url) for url in index_urls))
            index_urls = []
        return PackageFinder(find_links=options.find_links, format_control=options.format_control, index_urls=index_urls, trusted_hosts=options.trusted_hosts, allow_all_prereleases=options.pre, session=session, platform=platform, versions=python_versions, abi=abi, implementation=implementation, prefer_binary=options.prefer_binary)