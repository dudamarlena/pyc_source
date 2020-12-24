# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yapsy/ConfigurablePluginManager.py
# Compiled at: 2017-01-29 12:38:55
# Size of source mod 2**32: 10674 bytes
"""
Role
====

Defines plugin managers that can handle configuration files similar to
the ini files manipulated by Python's ConfigParser module.

API
===
"""
from yapsy.IPlugin import IPlugin
from yapsy.PluginManagerDecorator import PluginManagerDecorator
from yapsy.PluginManager import PLUGIN_NAME_FORBIDEN_STRING

class ConfigurablePluginManager(PluginManagerDecorator):
    __doc__ = "\n\tA plugin manager that also manages a configuration file.\n\n\tThe configuration file will be accessed through a ``ConfigParser``\n\tderivated object. The file can be used for other purpose by the\n\tapplication using this plugin manager as it will only add a new\n\tspecific section ``[Plugin Management]`` for itself and also new\n\tsections for some plugins that will start with ``[Plugin:...]``\n\t(only the plugins that explicitly requires to save configuration\n\toptions will have this kind of section).\n\n\t.. warning:: when giving/building the list of plugins to activate\n\t             by default, there must not be any space in the list\n\t             (neither in the names nor in between)\n\n\tThe ``config_change_trigger`` argument can be used to set a\n\tspecific method to call when the configuration is\n\taltered. This will let the client application manage the way\n\tthey want the configuration to be updated (e.g. write on file\n\tat each change or at precise time intervalls or whatever....)\n\t\n\t.. warning:: when no ``config_change_trigger`` is given and if\n\t             the provided ``configparser_instance`` doesn't handle it\n\t             implicitely, recording the changes persistently (ie writing on \n\t             the config file) won't happen.\n\t"
    CONFIG_SECTION_NAME = 'Plugin Management'

    def __init__(self, configparser_instance=None, config_change_trigger=lambda : True, decorated_manager=None, categories_filter=None, directories_list=None, plugin_info_ext='yapsy-plugin'):
        if categories_filter is None:
            categories_filter = {'Default': IPlugin}
        PluginManagerDecorator.__init__(self, decorated_manager, categories_filter, directories_list, plugin_info_ext)
        self.setConfigParser(configparser_instance, config_change_trigger)

    def setConfigParser(self, configparser_instance, config_change_trigger):
        """
                Set the ConfigParser instance.
                """
        self.config_parser = configparser_instance
        self.config_has_changed = config_change_trigger

    def __getCategoryPluginsListFromConfig(self, plugin_list_str):
        """
                Parse the string describing the list of plugins to activate,
                to discover their actual names and return them.
                """
        return plugin_list_str.strip(' ').split('%s' % PLUGIN_NAME_FORBIDEN_STRING)

    def __getCategoryPluginsConfigFromList(self, plugin_list):
        """
                Compose a string describing the list of plugins to activate
                """
        return PLUGIN_NAME_FORBIDEN_STRING.join(plugin_list)

    def __getCategoryOptionsName(self, category_name):
        """
                Return the appropirately formated version of the category's
                option.
                """
        return '%s_plugins_to_load' % category_name.replace(' ', '_')

    def __addPluginToConfig(self, category_name, plugin_name):
        """
                Utility function to add a plugin to the list of plugin to be
                activated.
                """
        if not self.config_parser.has_section(self.CONFIG_SECTION_NAME):
            self.config_parser.add_section(self.CONFIG_SECTION_NAME)
        else:
            option_name = self._ConfigurablePluginManager__getCategoryOptionsName(category_name)
            if not self.config_parser.has_option(self.CONFIG_SECTION_NAME, option_name):
                self.config_parser.set(self.CONFIG_SECTION_NAME, option_name, plugin_name)
                return self.config_has_changed()
            past_list_str = self.config_parser.get(self.CONFIG_SECTION_NAME, option_name)
            past_list = self._ConfigurablePluginManager__getCategoryPluginsListFromConfig(past_list_str)
            if plugin_name not in past_list:
                past_list.append(plugin_name)
                new_list_str = self._ConfigurablePluginManager__getCategoryPluginsConfigFromList(past_list)
                self.config_parser.set(self.CONFIG_SECTION_NAME, option_name, new_list_str)
                return self.config_has_changed()

    def __removePluginFromConfig(self, category_name, plugin_name):
        """
                Utility function to add a plugin to the list of plugin to be
                activated.
                """
        if not self.config_parser.has_section(self.CONFIG_SECTION_NAME):
            return
        else:
            option_name = self._ConfigurablePluginManager__getCategoryOptionsName(category_name)
            if not self.config_parser.has_option(self.CONFIG_SECTION_NAME, option_name):
                return
            past_list_str = self.config_parser.get(self.CONFIG_SECTION_NAME, option_name)
            past_list = self._ConfigurablePluginManager__getCategoryPluginsListFromConfig(past_list_str)
            if plugin_name in past_list:
                past_list.remove(plugin_name)
                new_list_str = self._ConfigurablePluginManager__getCategoryPluginsConfigFromList(past_list)
                self.config_parser.set(self.CONFIG_SECTION_NAME, option_name, new_list_str)
                self.config_has_changed()

    def registerOptionFromPlugin(self, category_name, plugin_name, option_name, option_value):
        """
                To be called from a plugin object, register a given option in
                the name of a given plugin.
                """
        section_name = '%s Plugin: %s' % (category_name, plugin_name)
        if not self.config_parser.has_section(section_name):
            self.config_parser.add_section(section_name)
        self.config_parser.set(section_name, option_name, option_value)
        self.config_has_changed()

    def hasOptionFromPlugin(self, category_name, plugin_name, option_name):
        """
                To be called from a plugin object, return True if the option
                has already been registered.
                """
        section_name = '%s Plugin: %s' % (category_name, plugin_name)
        return self.config_parser.has_section(section_name) and self.config_parser.has_option(section_name, option_name)

    def readOptionFromPlugin(self, category_name, plugin_name, option_name):
        """
                To be called from a plugin object, read a given option in
                the name of a given plugin.
                """
        section_name = '%s Plugin: %s' % (category_name, plugin_name)
        return self.config_parser.get(section_name, option_name)

    def __decoratePluginObject(self, category_name, plugin_name, plugin_object):
        """
                Add two methods to the plugin objects that will make it
                possible for it to benefit from this class's api concerning
                the management of the options.
                """
        plugin_object.setConfigOption = lambda x, y: self.registerOptionFromPlugin(category_name, plugin_name, x, y)
        plugin_object.setConfigOption.__doc__ = self.registerOptionFromPlugin.__doc__
        plugin_object.getConfigOption = lambda x: self.readOptionFromPlugin(category_name, plugin_name, x)
        plugin_object.getConfigOption.__doc__ = self.readOptionFromPlugin.__doc__
        plugin_object.hasConfigOption = lambda x: self.hasOptionFromPlugin(category_name, plugin_name, x)
        plugin_object.hasConfigOption.__doc__ = self.hasOptionFromPlugin.__doc__

    def activatePluginByName(self, plugin_name, category_name='Default', save_state=True):
        """
                Activate a plugin, , and remember it (in the config file).

                If you want the plugin to benefit from the configuration
                utility defined by this manager, it is crucial to use this
                method to activate a plugin and not call the plugin object's
                ``activate`` method. In fact, this method will also "decorate"
                the plugin object so that it can use this class's methods to
                register its own options.
                
                By default, the plugin's activation is registered in the
                config file but if you d'ont want this set the 'save_state'
                argument to False.
                """
        pta = self._component.getPluginByName(plugin_name, category_name)
        if pta is None:
            return
        self._ConfigurablePluginManager__decoratePluginObject(category_name, plugin_name, pta.plugin_object)
        plugin_object = self._component.activatePluginByName(plugin_name, category_name)
        if plugin_object.is_activated:
            if save_state:
                self._ConfigurablePluginManager__addPluginToConfig(category_name, plugin_name)
            return plugin_object

    def deactivatePluginByName(self, plugin_name, category_name='Default', save_state=True):
        """
                Deactivate a plugin, and remember it (in the config file).

                By default, the plugin's deactivation is registered in the
                config file but if you d'ont want this set the ``save_state``
                argument to False.
                """
        plugin_object = self._component.deactivatePluginByName(plugin_name, category_name)
        if plugin_object is None:
            return
        if not plugin_object.is_activated:
            if save_state:
                self._ConfigurablePluginManager__removePluginFromConfig(category_name, plugin_name)
                return plugin_object

    def loadPlugins(self, callback=None, callback_after=None):
        """
                Walk through the plugins' places and look for plugins.  Then
                for each plugin candidate look for its category, load it and
                stores it in the appropriate slot of the ``category_mapping``.
                """
        self._component.loadPlugins(callback, callback_after)
        if self.config_parser.has_section(self.CONFIG_SECTION_NAME):
            for category_name in list(self._component.category_mapping.keys()):
                option_name = '%s_plugins_to_load' % category_name
                if self.config_parser.has_option(self.CONFIG_SECTION_NAME, option_name):
                    plugin_list_str = self.config_parser.get(self.CONFIG_SECTION_NAME, option_name)
                    plugin_list = self._ConfigurablePluginManager__getCategoryPluginsListFromConfig(plugin_list_str)
                    for plugin_name in plugin_list:
                        self.activatePluginByName(plugin_name, category_name)