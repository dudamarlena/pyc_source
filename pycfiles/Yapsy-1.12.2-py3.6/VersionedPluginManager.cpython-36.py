# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/VersionedPluginManager.py
# Compiled at: 2017-01-29 12:38:39
# Size of source mod 2**32: 3998 bytes
"""
Role
====

Defines the basic interface for a plugin manager that also keeps track
of versions of plugins

API
===
"""
from distutils.version import StrictVersion
from yapsy.PluginInfo import PluginInfo
from yapsy.IPlugin import IPlugin
from yapsy.PluginManagerDecorator import PluginManagerDecorator

class VersionedPluginInfo(PluginInfo):
    __doc__ = '\n\tGather some info about a plugin such as its name, author,\n\tdescription...\n\t'

    def __init__(self, plugin_name, plugin_path):
        PluginInfo.__init__(self, plugin_name, plugin_path)
        self.version = StrictVersion('0.0')

    def setVersion(self, vstring):
        self.version = StrictVersion(vstring)


class VersionedPluginManager(PluginManagerDecorator):
    __doc__ = '\n\tHandle plugin versioning by making sure that when several\n\tversions are present for a same plugin, only the latest version is\n\tmanipulated via the standard methods (eg for activation and\n\tdeactivation)\n\t\n\tMore precisely, for operations that must be applied on a single\n\tnamed plugin at a time (``getPluginByName``,\n\t``activatePluginByName``, ``deactivatePluginByName`` etc) the\n\ttargetted plugin will always be the one with the latest version.\n\t\n\t.. note:: The older versions of a given plugin are still reachable\n\t          via the ``getPluginsOfCategoryFromAttic`` method.\n\t'

    def __init__(self, decorated_manager=None, categories_filter={'Default': IPlugin}, directories_list=None, plugin_info_ext='yapsy-plugin'):
        PluginManagerDecorator.__init__(self, decorated_manager, categories_filter, directories_list, plugin_info_ext)
        self.setPluginInfoClass(VersionedPluginInfo)
        self._prepareAttic()

    def _prepareAttic(self):
        """
                Create and correctly initialize the storage where the wrong
                version of the plugins will be stored.
                """
        self._attic = {}
        for categ in self.getCategories():
            self._attic[categ] = []

    def setCategoriesFilter(self, categories_filter):
        """
                Set the categories of plugins to be looked for as well as the
                way to recognise them.

                Note: will also reset the attic toa void inconsistencies.
                """
        self._component.setCategoriesFilter(categories_filter)
        self._prepareAttic()

    def getLatestPluginsOfCategory(self, category_name):
        """
                DEPRECATED(>1.8): Please consider using getPluginsOfCategory
                instead.
                
                Return the list of all plugins belonging to a category.
                """
        return self.getPluginsOfCategory(category_name)

    def loadPlugins(self, callback=None, callback_after=None):
        """
                Load the candidate plugins that have been identified through a
                previous call to locatePlugins.

                In addition to the baseclass functionality, this subclass also
                needs to find the latest version of each plugin.
                """
        self._prepareAttic()
        self._component.loadPlugins(callback, callback_after)
        for categ in self.getCategories():
            latest_plugins = {}
            allPlugins = self.getPluginsOfCategory(categ)
            for plugin in allPlugins:
                name = plugin.name
                version = plugin.version
                if name in latest_plugins:
                    if version > latest_plugins[name].version:
                        older_plugin = latest_plugins[name]
                        latest_plugins[name] = plugin
                        self.removePluginFromCategory(older_plugin, categ)
                        self._attic[categ].append(older_plugin)
                    else:
                        self.removePluginFromCategory(plugin, categ)
                        self._attic[categ].append(plugin)
                else:
                    latest_plugins[name] = plugin

    def getPluginsOfCategoryFromAttic(self, categ):
        """
                Access the older version of plugins for which only the latest
                version is available through standard methods.
                """
        return self._attic[categ]