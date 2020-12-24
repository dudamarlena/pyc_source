# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/managers/importmanager.py
# Compiled at: 2013-11-08 09:23:49
"""
Manager of external results import plugins.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'ImportManager']
from ..api.config import Config
from ..api.logger import Logger
from traceback import format_exc

class ImportManager(object):
    """
    Manager of external results importer plugins.
    """

    def __init__(self, orchestrator, audit):
        """
        :param orchestrator: Orchestrator instance.
        :type orchestrator: Orchestrator

        :param audit: Audit instance.
        :type audit: Audit
        """
        self.__config = audit.config
        self.__orchestrator = orchestrator
        self.__plugins = audit.pluginManager.load_plugins('import')
        self.__importers = {}
        for input_file in self.__config.imports:
            if input_file in self.__importers:
                continue
            found = [ name for name, plugin in self.__plugins.iteritems() if plugin.is_supported(input_file)
                    ]
            if not found:
                raise ValueError('Input file format not supported: %r' % input_file)
            if len(found) > 1:
                msg = 'Input file format supported by multiple plugins!\nFile: %r\nPlugins:\n\t'
                msg %= input_file
                msg += ('\n\t').join(found)
                raise ValueError(msg)
            self.__importers[input_file] = found[0]

    @property
    def is_enabled(self):
        """
        :returns: True if there are active importers, False otherwise.
        :rtype: bool
        """
        return bool(self.__importers)

    @property
    def config(self):
        """
        :returns: Audit configuration.
        :rtype: AuditConfig.
        """
        return self.__config

    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance.
        :rtype: Orchestrator
        """
        return self.__orchestrator

    @property
    def plugin_count(self):
        """
        :returns: Number of import plugins loaded.
        :rtype: int
        """
        return len(self.__importers)

    def import_results(self):
        """
        Import all the requested results before running an audit.

        :returns: Number of plugins executed.
        :rtype: int
        """
        if not self.__importers:
            return 0
        else:
            Logger.log_verbose('Importing results from external tools...')
            count = 0
            for input_file, plugin_id in self.__importers.iteritems():
                try:
                    plugin_instance = self.__plugins[plugin_id]
                    context = self.orchestrator.build_plugin_context(self.config.audit_name, plugin_instance, None)
                    old_context = Config._context
                    try:
                        Config._context = context
                        plugin_instance.import_results(input_file)
                    finally:
                        Config._context = old_context

                except Exception as e:
                    Logger.log_error('Failed to import results from file %r: %s' % (
                     input_file, str(e)))
                    Logger.log_error_more_verbose(format_exc())

                count += 1

            return count

    def close(self):
        """
        Release all resources held by this manager.
        """
        self.__config = None
        self.__orchestrator = None
        self.__plugins = None
        self.__importers = None
        return