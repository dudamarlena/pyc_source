# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\__init__.py
# Compiled at: 2018-07-06 18:13:01
# Size of source mod 2**32: 11267 bytes
import sys, os, platform
from pathlib import Path
from appdirs import user_config_dir, site_config_dir, user_cache_dir
from yapsy import PluginInfo
from yapsy.PluginManager import PluginManager
from xicam.core import msg
from .DataHandlerPlugin import DataHandlerPlugin
from .GUIPlugin import GUIPlugin, GUILayout
from .ProcessingPlugin import ProcessingPlugin, EZProcessingPlugin, Input, Output, InOut
from .SettingsPlugin import SettingsPlugin
from .DataResourcePlugin import DataResourcePlugin
from .WidgetPlugin import QWidgetPlugin
from .venvs import observers as venvsobservers
from .DataResourcePlugin import DataResourcePlugin
from .FittableModelPlugin import Fittable1DModelPlugin
from .EZPlugin import _EZPlugin, EZPlugin
from .hint import PlotHint, Hint
from yapsy.PluginManager import NormalizePluginNameForModuleName, imp, log
import xicam
op_sys = platform.system()
if op_sys == 'Darwin':
    user_plugin_dir = os.path.join(user_cache_dir(appname='xicam'), 'plugins')
else:
    user_plugin_dir = os.path.join(user_config_dir(appname='xicam'), 'plugins')
site_plugin_dir = os.path.join(site_config_dir(appname='xicam'), 'plugins')
observers = []
qt_is_safe = False
if 'qtpy' in sys.modules:
    from qtpy.QtWidgets import QApplication
    if QApplication.instance():
        qt_is_safe = True

class XicamPluginManager(PluginManager):

    def __init__(self):
        super(XicamPluginManager, self).__init__()
        venvsobservers.append(self)
        categoriesfilter = {'DataHandlerPlugin':DataHandlerPlugin, 
         'DataResourcePlugin':DataResourcePlugin, 
         'ProcessingPlugin':ProcessingPlugin, 
         'Fittable1DModelPlugin':Fittable1DModelPlugin}
        if qt_is_safe:
            categoriesfilter.update({'GUIPlugin':GUIPlugin,  'WidgetPlugin':QWidgetPlugin, 
             'SettingsPlugin':SettingsPlugin, 
             'EZPlugin':_EZPlugin, 
             'Fittable1DModelPlugin':Fittable1DModelPlugin})
        self.setCategoriesFilter(categoriesfilter)
        self.setPluginPlaces([
         os.getcwd(), str(Path(__file__).parent.parent), user_plugin_dir, site_plugin_dir,
         venvs.current_environment] + list(xicam.__path__))
        self.loadcomplete = False

    def collectPlugins(self):
        """
        Walk through the plugins' places and look for plugins.  Then
        for each plugin candidate look for its category, load it and
        stores it in the appropriate slot of the category_mapping.

        Overloaded to add callback.
        """
        self.locatePlugins()
        candidatedict = {c[2].name:c[2] for c in self._candidates}
        candidatesset = candidatedict.values()
        for plugin in self._candidates:
            if plugin[2] not in candidatesset:
                msg.logMessage(f'Possible duplicate plugin name "{plugin[2].name}" at {plugin[2].path}', level=(msg.WARNING))
                msg.logMessage(f"Possibly shadowed by {candidatedict[plugin[2].name].path}", level=(msg.WARNING))

        self.loadPlugins(callback=(self.showLoading))
        self.instanciateLatePlugins()
        for observer in observers:
            observer.pluginsChanged()

        self.loadcomplete = True

    def instanciateLatePlugins(self):
        if qt_is_safe:
            for plugin_info in self.getPluginsOfCategory('GUIPlugin'):
                if callable(plugin_info.plugin_object):
                    try:
                        plugin_info.plugin_object = plugin_info.plugin_object()
                    except Exception as ex:
                        msg.notifyMessage(f'The "{plugin_info.name}" plugin could not be loaded. {repr(ex)}', level=(msg.CRITICAL))
                        msg.logError(ex)

    def instanciateElement(self, element):
        """
        The default behavior is that each plugin is instanciated at load time; the class is thrown away.
        Add the isSingleton = False attribute to your plugin class to prevent this behavior!
        """
        if getattr(element, 'isSingleton', True):
            return element()
        else:
            return element

    def showLoading(self, plugininfo: PluginInfo):
        name = plugininfo.name
        msg.logMessage(f"Loading {name} from {plugininfo.path}")

    def venvChanged(self):
        self.setPluginPlaces([venvs.current_environment])
        self.collectPlugins()

    def __getitem__(self, item: str):
        """
        Convenient way to get plugins.

        Usage
        -----

        manager['GUIPlugin']['SAXS']

        """
        return {plugin.name:plugin for plugin in self.getPluginsOfCategory(item)}

    def loadPlugins(self, callback=None):
        """
        Load the candidate plugins that have been identified through a
        previous call to locatePlugins.  For each plugin candidate
        look for its category, load it and store it in the appropriate
        slot of the ``category_mapping``.

        If a callback function is specified, call it before every load
        attempt.  The ``plugin_info`` instance is passed as an argument to
        the callback.
        """
        if not hasattr(self, '_candidates'):
            raise ValueError('locatePlugins must be called before loadPlugins')
        processed_plugins = []
        for candidate_infofile, candidate_filepath, plugin_info in self._candidates:
            plugin_module_name_template = NormalizePluginNameForModuleName('yapsy_loaded_plugin_' + plugin_info.name) + '_%d'
            for plugin_name_suffix in range(len(sys.modules)):
                plugin_module_name = plugin_module_name_template % plugin_name_suffix
                if plugin_module_name not in sys.modules:
                    break

            if candidate_filepath.endswith('.py'):
                candidate_filepath = candidate_filepath[:-3]
            if callback is not None:
                callback(plugin_info)
            if '__init__' in os.path.basename(candidate_filepath):
                candidate_filepath = os.path.dirname(candidate_filepath)
            try:
                if os.path.isdir(candidate_filepath):
                    candidate_module = imp.load_module(plugin_module_name, None, candidate_filepath, (
                     'py', 'r', imp.PKG_DIRECTORY))
                else:
                    with open(candidate_filepath + '.py', 'r') as (plugin_file):
                        candidate_module = imp.load_module(plugin_module_name, plugin_file, candidate_filepath + '.py', ('py', 'r', imp.PY_SOURCE))
            except Exception:
                exc_info = sys.exc_info()
                log.error(('Unable to import plugin: %s' % candidate_filepath), exc_info=exc_info)
                plugin_info.error = exc_info
                processed_plugins.append(plugin_info)
                continue

            processed_plugins.append(plugin_info)
            if '__init__' in os.path.basename(candidate_filepath):
                sys.path.remove(plugin_info.path)
            dirlist = dir(candidate_module)
            if hasattr(candidate_module, '__plugin_exports__'):
                dirlist = candidate_module.__plugin_exports__
            for element in (getattr(candidate_module, name) for name in dirlist):
                plugin_info_reference = None
                for category_name in self.categories_interfaces:
                    try:
                        is_correct_subclass = issubclass(element, self.categories_interfaces[category_name])
                    except Exception:
                        continue

                    if is_correct_subclass:
                        if element is not self.categories_interfaces[category_name]:
                            current_category = category_name
                            if candidate_infofile not in self._category_file_mapping[current_category]:
                                if not plugin_info_reference:
                                    try:
                                        plugin_info.plugin_object = self.instanciateElement(element)
                                        plugin_info_reference = plugin_info
                                    except Exception:
                                        exc_info = sys.exc_info()
                                        log.error(('Unable to create plugin object: %s' % candidate_filepath), exc_info=exc_info)
                                        plugin_info.error = exc_info
                                        break

                        plugin_info.categories.append(current_category)
                        self.category_mapping[current_category].append(plugin_info_reference)
                        self._category_file_mapping[current_category].append(candidate_infofile)

        delattr(self, '_candidates')
        return processed_plugins


manager = XicamPluginManager()
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions