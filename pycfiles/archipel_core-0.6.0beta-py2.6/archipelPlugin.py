# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelcore/archipelPlugin.py
# Compiled at: 2013-03-20 13:50:16


class TNArchipelPlugin:

    def __init__(self, configuration=None, entity=None, entry_point_group=None):
        """
        Initialize the plugin.
        @type configuration: Configuration object
        @param configuration: the configuration
        @type entity: L{TNArchipelEntity}
        @param entity: the entity that owns the plugin
        @type entry_point_group: string
        @param entry_point_group: the group name of plugin entry_point
        """
        self.configuration = configuration
        self.entity = entity
        self.plugin_entry_point_group = entry_point_group

    def register_handlers(self):
        """
        This method will be called to when entiyt will register
        handlers for stanzas. Place plugin handlers registration here.
        """
        pass

    def unregister_handlers(self):
        """
        Unregister the handlers. This method must be implemented if register_handlers
        is implemented.
        """
        pass

    @classmethod
    def plugin_info(self, group):
        """
        Return plugin information. it must return a dict like:
        plugin_friendly_name           = "User friendly name of plugin"
        plugin_identifier              = "plugin_identifier"
        plugin_configuration_section   = "required [SECTION] in configuration"
        plugin_configuration_tokens    = [  "required_token_section1",
                                            "required_token_section2"]
        return {    "common-name"               : plugin_friendly_name,
                    "identifier"                : plugin_identifier,
                    "configuration-section"     : plugin_configuration_section,
                    "configuration-tokens"      : plugin_configuration_tokens }
        @raise Exception: Exception if not implemented
        """
        raise Exception("plugins objects must implement 'plugin_info'")