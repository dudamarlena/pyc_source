# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plugboard/plugin.py
# Compiled at: 2006-02-21 15:01:34
from zope import interface
import pkg_resources, types, traceback

class IPlugin(interface.Interface):
    """
    A basic interface for allkind of plugins
    """
    __module__ = __name__
    dispatcher = interface.Attribute('An IEventDispatcher object to let other plugins connect to the plugin trough events')
    application = interface.Attribute('Automatically set when initializing the plugin')
    context = interface.Attribute('Automatically set when loading the plugin into the current context')
    plugin = interface.Attribute('Automatically set when creating a new instance of the plugin to be plugged into another one')

    def preload(context):
        """
        Called before loading the plugin
        """
        pass

    def load(context):
        """
        Load plugin in the current context
        """
        pass

    def plug(plugin):
        """
        Plug the plugin into another plugin
        """
        pass

    def unload(context):
        """
        Unload plugin from the current context
        """
        pass

    def unplug(plugin):
        """
        Unplug the plugin from another plugin
        """
        pass


class IPluginResource(interface.Interface):
    """
    Application plugin control which contains all available plugins
    """
    __module__ = __name__

    def get_plugins():
        """
        Returns the list of detected plugins
        """
        pass

    get_plugins.return_type = types.GeneratorType

    def refresh():
        """
        Refresh the list of plugins
        """
        pass


class Plugin(object):
    __module__ = __name__
    interface.implements(IPlugin)

    def __init__(self, application):
        pass

    def preload(self, context):
        pass

    def load(self, context):
        pass

    def plug(self, plugin):
        pass

    def unload(self, context):
        pass

    def unplug(self, plugin):
        pass


class PluginResource(object):
    __module__ = __name__
    interface.implements(IPluginResource)

    def __init__(self, application):
        self.application = application
        self._plugins = set()
        application.register(application, self)

    def get_plugins(self):
        return iter(self._plugins)

    def refresh(self):
        raise NotImplementedError


class SetuptoolsPluginResource(PluginResource):
    __module__ = __name__

    def __init__(self, application, entrypoint_path):
        super(SetuptoolsPluginResource, self).__init__(application)
        self.entrypoint_path = entrypoint_path

    def refresh(self, entrypoint_path=None):
        if entrypoint_path is not None:
            self.entrypoint_path = entrypoint_path
        self._plugins.clear()
        for entrypoint in pkg_resources.iter_entry_points(self.entrypoint_path):
            try:
                plugin_class = entrypoint.load()
            except:
                traceback.print_exc()
                continue

            self._plugins.add(plugin_class)

        return


__all__ = ['IPlugin', 'IPluginResource', 'Plugin', 'PluginResource']