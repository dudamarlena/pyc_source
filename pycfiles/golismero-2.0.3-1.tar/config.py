# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/config.py
# Compiled at: 2014-01-11 11:02:01
"""
Plugin configuration API.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'Config', 'get_orchestrator_config']
from ..common import Singleton
from ..messaging.codes import MessageCode
import threading

def get_orchestrator_config():
    """
    :returns: Orchestrator configuration.
    :rtype: OrchestratorConfig
    """
    return Config._context.remote_call(MessageCode.MSG_RPC_AUDIT_CONFIG, None)


class _Config(Singleton):
    """
    Current plugin and audit configuration.

    Whenever a plugin accesses this object it will receive its own
    configuration, including the current audit's name and settings.

    Example:

        >>> from golismero.api.config import Config
        >>> Config.plugin_id
        'my_plugin_id'
    """

    def __init__(self):
        try:
            Config
            raise NotImplementedError('Use Config instead!')
        except NameError:
            pass

        self.__thread_local = threading.local()

    @property
    def audit_name(self):
        """
        :returns: Name of the audit.
        :rtype: str
        """
        return self._context.audit_name

    @property
    def audit_config(self):
        """
        :returns: Parameters of the audit.
        :rtype: AuditConfig
        """
        return self._context.audit_config

    @property
    def audit_scope(self):
        """
        :returns: Scope of the audit.
        :rtype: AuditScope
        """
        return self._context.audit_scope

    @property
    def plugin_info(self):
        """
        :returns: Plugin information.
        :rtype: PluginInfo
        """
        return self._context.plugin_info

    @property
    def plugin_id(self):
        """
        :returns: Plugin ID.
        :rtype: str
        """
        return self.plugin_info.plugin_id

    @property
    def plugin_module(self):
        """
        :returns: Module where the plugin was loaded from.
        :rtype: str
        """
        return self.plugin_info.plugin_module

    @property
    def plugin_class(self):
        """
        :returns: Class name of the plugin.
        :rtype: str
        """
        return self.plugin_info.plugin_class

    @property
    def plugin_args(self):
        """
        Plugin arguments.

        Here you will find all settings under the [Arguments]
        section in the plugin configuration file.

        :returns:
        :rtype: dict(str -> str)
        """
        return self.plugin_info.plugin_args

    @property
    def plugin_config(self):
        """
        Plugin configuration.

        Here you will find all settings under the [Configuration]
        section in the plugin configuration file.

        :returns:
        :rtype: dict(str -> str)
        """
        return self.plugin_info.plugin_config

    @property
    def plugin_extra_config(self):
        """
        Plugin extra configuration.

        Here you will find all information in the plugin
        configuration file outside the following sections:

        - [Core]
        - [Documentation]
        - [Arguments]
        - [Configuration]

        >>> from golismero.api.config import Config
        >>> print open("suspicious_url.golismero").read()
        [Core]
        Name = Suspicious URL
        Module = suspicious_url.py
        Stage = Recon
        [Documentation]
        Description = Find suspicious words in URLs
        Author = Daniel Garcia Garcia (cr0hn)
        Version = 0.1
        Website = https://github.com/golismero
        Copyright = Copyright (C) 2011-2014 GoLismero Project
        License = GNU Public License
        [Wordlist_middle]
        wordlist = golismero/warning_url.txt
        [Wordlist_extensions]
        wordlist = fuzzdb/Discovery/FilenameBruteforce/Extensions.Backup.fuzz.txt
        >>> Config.plugin_extra_config['Wordlist_middle']['wordlist']
        'golismero/warning_url.txt'
        >>> Config.plugin_extra_config['Wordlist_extensions']['wordlist']
        'fuzzdb/Discovery/FilenameBruteforce/Extensions.Backup.fuzz.txt'

        :returns: Map of configuration file sections to their settings and values.
        :rtype: dict(str -> dict(str -> str))
        """
        return self.plugin_info.plugin_extra_config

    @property
    def depth(self):
        """"
        :returns: Current analysis depth.
        :rtype: int
        """
        return self._context._depth

    @property
    def _context(self):
        """
        .. warning: Internally used by GoLismero. Do not use it in plugins!

        :rtype: PluginContext
        """
        try:
            return self.__thread_local.context
        except AttributeError:
            raise SyntaxError('Plugin execution environment not initialized')

    @_context.setter
    def _context(self, context):
        """
        .. warning: Internally used by GoLismero. Do not use it in plugins!

        :type context: PluginContext
        """
        self.__thread_local.context = context

    @property
    def _has_context(self):
        """
        :returns: True if the plugin execution environment is initialized, False otherwise.
        :rtype: bool
        """
        try:
            self.__thread_local.context
            return True
        except AttributeError:
            return False


Config = _Config()