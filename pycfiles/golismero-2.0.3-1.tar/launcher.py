# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/main/launcher.py
# Compiled at: 2014-01-11 11:02:01
"""
GoLismero launcher.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'run']
from .console import Console
from .orchestrator import Orchestrator
from ..api.net.web_utils import detect_auth_method, check_auth
from ..common import OrchestratorConfig, AuditConfig, get_default_config_file, get_default_user_config_file
import datetime, traceback

def run(options, *audits):
    """
    Runs GoLismero in the current process.

    Optionally starts the requested audits. Pass each audit configuration
    object as a positional argument.

    Returns when (if) GoLismero finishes executing.

    :param options: Orchestrator settings.
    :type options: OrchestratorConfig

    :param audits: Audit settings.
    :type audits: AuditConfig

    :returns: Exit code.
    :rtype: int

    :raises AttributeError: A critical configuration option is missing.
    :raises TypeError: A configuration option has a value of a wrong type.
    :raises ValueError: A configuration option has an incorrect value.
    :raises Exception: An error occurred while validating the settings.
    """
    options, audits = _sanitize_config(options, audits)
    Console.level = options.verbose
    Console.use_colors = options.color
    Console.display('GoLismero started at %s UTC' % datetime.datetime.utcnow())
    try:
        return_code = _run(options, *audits)
    except KeyboardInterrupt:
        Console.display('GoLismero cancelled by the user at %s UTC' % datetime.datetime.utcnow())
        return 1
    except SystemExit as e:
        Console.display('GoLismero stopped at %s UTC' % datetime.datetime.utcnow())
        return e.code

    Console.display('GoLismero finished at %s UTC' % datetime.datetime.utcnow())
    return return_code


def _run(options, *audits):
    try:
        for auditParams in audits:
            try:
                proxy_addr = auditParams.proxy_addr
                if proxy_addr:
                    proxy_port = auditParams.proxy_port
                    if proxy_port:
                        proxy_addr = '%s:%s' % (proxy_addr, proxy_port)
                    proxy_addr = 'http://' + proxy_addr
                    if auditParams.proxy_user:
                        if not check_auth(proxy_addr, auditParams.proxy_user, auditParams.proxy_pass):
                            tb = traceback.format_exc()
                            Console.display_error('[!] Authentication failed for proxy: %r' % proxy_addr)
                            Console.display_error_more_verbose(tb)
                            return 1
                    else:
                        auth, _ = detect_auth_method(proxy_addr)
                        if auth:
                            tb = traceback.format_exc()
                            Console.display_error('[!] Authentication required for proxy: %r' % proxy_addr)
                            Console.display_error("Use '--proxy-user' and '--proxy-pass' to set the username and password.")
                            Console.display_error_more_verbose(tb)
                            return 1
            except Exception as e:
                tb = traceback.format_exc()
                Console.display_error('[!] Proxy settings failed, reason: %s' % str(e))
                Console.display_error_more_verbose(tb)
                return 1

        while True:
            with Orchestrator(options) as (orchestrator):
                try:
                    orchestrator.uiManager.check_params(*audits)
                except SystemExit:
                    return 1
                except Exception as e:
                    Console.display_error('[!] Configuration error: %s' % str(e))
                    Console.display_error_more_verbose(traceback.format_exc())
                    if orchestrator.config.ui_mode != 'daemon':
                        return 1
                    continue

                try:
                    orchestrator.run(*audits)
                except SystemExit:
                    return 1
                except Exception as e:
                    Console.display_error(e)
                    if orchestrator.config.ui_mode != 'daemon':
                        return 1
                    continue

    except SystemExit:
        return 1
    except Exception as e:
        Console.display_error('[!] Fatal error! %s' % str(e))
        Console.display_error_more_verbose(traceback.format_exc())
        return 1


def _sanitize_config(options, audits):
    """
    Validate and sanitize the arguments to the launcher.

    :param options: Orchestrator settings.
    :type options: OrchestratorConfig

    :param audits: Audit settings.
    :type audits: AuditConfig

    :returns: Sanitized options.
    :rtype: tuple(OrchestratorConfig, tuple(AuditConfig...))

    :raise TypeError: Bad argument types.
    """
    if options is None:
        options = OrchestratorConfig()
    else:
        if not isinstance(options, OrchestratorConfig):
            raise TypeError('Expected OrchestratorConfig, got %r instead' % type(options))
        if not hasattr(options, 'profile'):
            options.profile = None
            options.profile_file = None
        if not hasattr(options, 'config_file'):
            options.config_file = get_default_config_file()
        if not hasattr(options, 'user_config_file'):
            options.user_config_file = get_default_user_config_file()
        if not hasattr(options, 'plugin_load_overrides'):
            options.plugin_load_overrides = []
        options.check_params()
        sane_audits = []
        for params in audits:
            if params is None:
                params = AuditConfig()
            elif not isinstance(params, AuditConfig):
                raise TypeError('Expected AuditConfig, got %r instead' % type(params))
            if not hasattr(params, 'profile'):
                params.profile = options.profile
                params.profile_file = options.profile_file
            if not hasattr(params, 'config_file'):
                params.config_file = options.config_file
            if not hasattr(params, 'user_config_file'):
                params.user_config_file = options.user_config_file
            if not hasattr(params, 'plugin_load_overrides'):
                params.plugin_load_overrides = options.plugin_load_overrides
            if not hasattr(params, 'targets') or not params.targets:
                if hasattr(options, 'targets'):
                    params.targets = list(options.targets)
            params.check_params()
            sane_audits.append(params)

    return (options, tuple(sane_audits))