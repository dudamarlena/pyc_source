# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/basecommand.py
# Compiled at: 2019-09-10 15:18:29
"""Base Command class, and related routines"""
from __future__ import absolute_import
import logging, logging.config, optparse, os, sys
from pip._internal import cmdoptions
from pip._internal.baseparser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.download import PipSession
from pip._internal.exceptions import BadCommand, CommandError, InstallationError, PreviousBuildDirError, UninstallationError
from pip._internal.index import PackageFinder
from pip._internal.locations import running_under_virtualenv
from pip._internal.req.req_file import parse_requirements
from pip._internal.req.req_install import InstallRequirement
from pip._internal.status_codes import ERROR, PREVIOUS_BUILD_DIR_ERROR, SUCCESS, UNKNOWN_ERROR, VIRTUALENV_NOT_FOUND
from pip._internal.utils.logging import setup_logging
from pip._internal.utils.misc import get_prog, normalize_path
from pip._internal.utils.outdated import pip_version_check
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional
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
        setup_logging(verbosity=self.verbosity, no_color=options.no_color, user_log_file=options.log)
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
            except KeyboardInterrupt:
                logger.critical('Operation cancelled by user')
                logger.debug('Exception information:', exc_info=True)
                return ERROR
            except BaseException:
                logger.critical('Exception:', exc_info=True)
                return UNKNOWN_ERROR

        finally:
            skip_version_check = options.disable_pip_version_check or getattr(options, 'no_index', False)
            if not skip_version_check:
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
            req_to_add = InstallRequirement.from_line(req, None, isolated=options.isolated_mode, wheel_cache=wheel_cache)
            req_to_add.is_direct = True
            requirement_set.add_requirement(req_to_add)

        for req in options.editables:
            req_to_add = InstallRequirement.from_editable(req, isolated=options.isolated_mode, wheel_cache=wheel_cache)
            req_to_add.is_direct = True
            requirement_set.add_requirement(req_to_add)

        for filename in options.requirements:
            for req_to_add in parse_requirements(filename, finder=finder, options=options, session=session, wheel_cache=wheel_cache):
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
            logger.debug('Ignoring indexes: %s', (',').join(index_urls))
            index_urls = []
        return PackageFinder(find_links=options.find_links, format_control=options.format_control, index_urls=index_urls, trusted_hosts=options.trusted_hosts, allow_all_prereleases=options.pre, process_dependency_links=options.process_dependency_links, session=session, platform=platform, versions=python_versions, abi=abi, implementation=implementation, prefer_binary=options.prefer_binary)