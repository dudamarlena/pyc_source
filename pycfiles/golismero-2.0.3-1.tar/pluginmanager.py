# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/managers/pluginmanager.py
# Compiled at: 2014-01-11 11:02:01
"""
'Priscilla', the GoLismero plugin manager.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'PluginManager', 'PluginInfo']
from .rpcmanager import implementor
from ..api.config import Config
from ..api.logger import Logger
from ..api.plugin import CATEGORIES, STAGES, load_plugin_class_from_info
from ..common import Configuration, OrchestratorConfig, AuditConfig, get_default_plugins_folder, EmptyNewStyleClass
from ..managers.processmanager import PluginContext
from ..messaging.codes import MessageCode
from collections import defaultdict
from ConfigParser import RawConfigParser
from keyword import iskeyword
from os import path, walk
import re, fnmatch, traceback, warnings

@implementor(MessageCode.MSG_RPC_PLUGIN_GET_IDS)
def rpc_plugin_get_ids(orchestrator, audit_name, *args, **kwargs):
    if audit_name:
        audit = orchestrator.auditManager.get_audit(audit_name)
        try:
            return audit.pluginManager.get_plugin_ids(*args, **kwargs)
        except KeyError:
            pass

    return orchestrator.pluginManager.get_plugin_ids(*args, **kwargs)


@implementor(MessageCode.MSG_RPC_PLUGIN_GET_INFO)
def rpc_plugin_get_info(orchestrator, audit_name, *args, **kwargs):
    if audit_name:
        audit = orchestrator.auditManager.get_audit(audit_name)
        try:
            return audit.pluginManager.get_plugin_by_id(*args, **kwargs)
        except KeyError:
            pass

    return orchestrator.pluginManager.get_plugin_by_id(*args, **kwargs)


class PluginInfo(object):
    """
    Plugin descriptor object.
    """

    @property
    def plugin_id(self):
        """
        :returns: Plugin ID.
        :rtype: str
        """
        return self.__plugin_id

    @property
    def descriptor_file(self):
        """
        :returns: Plugin descriptor file name.
        :rtype: str
        """
        return self.__descriptor_file

    @property
    def category(self):
        """
        :returns: Plugin category.
        :rtype: str
        """
        return self.__plugin_id.split('/')[0].lower()

    @property
    def stage(self):
        """
        :returns: Plugin stage name.
        :rtype: int
        """
        if self.category == 'testing':
            return PluginManager.get_stage_name_from_value(self.__stage_number)
        return self.category

    @property
    def stage_number(self):
        """
        :returns: Plugin stage number.
        :rtype: int
        """
        return self.__stage_number

    @property
    def dependencies(self):
        """
        :returns: Plugin dependencies.
        :rtype: tuple(str...)
        """
        return self.__dependencies

    @property
    def recursive(self):
        """
        :returns: True if the plugin is recursive, False otherwise.
        :rtype: bool
        """
        return self.__recursive

    @property
    def plugin_module(self):
        """
        :returns: Plugin module file name.
        :rtype: str
        """
        return self.__plugin_module

    @property
    def plugin_class(self):
        """
        :returns: Plugin class name.
        :rtype: str
        """
        return self.__plugin_class

    @property
    def plugin_args(self):
        """
        :returns: Plugin arguments.
        :rtype: dict(str -> str)
        """
        return self.__plugin_args

    @property
    def plugin_passwd_args(self):
        """
        :returns: Plugin password argument names.
        :rtype: set(str)
        """
        return self.__plugin_passwd_args

    @property
    def plugin_config(self):
        """
        :returns: Plugin configuration.
        :rtype: dict(str -> str)
        """
        return self.__plugin_config

    @property
    def plugin_extra_config(self):
        """
        :returns: Plugin extra configuration.
        :rtype: dict(str -> dict(str -> str))
        """
        return self.__plugin_extra_config

    @property
    def display_name(self):
        """
        :returns: Display name to be shown to the user.
        :rtype: str
        """
        return self.__display_name

    @property
    def description(self):
        """
        :returns: Description of this plugin's functionality.
        :rtype: str
        """
        return self.__description

    @property
    def version(self):
        """
        :returns: Version of this plugin.
        :rtype: str
        """
        return self.__version

    @property
    def author(self):
        """
        :returns: Author of this plugin.
        :rtype: str
        """
        return self.__author

    @property
    def copyright(self):
        """
        :returns: Copyright of this plugin.
        :rtype: str
        """
        return self.__copyright

    @property
    def license(self):
        """
        :returns: License for this plugin.
        :rtype: str
        """
        return self.__license

    @property
    def website(self):
        """
        :returns: Web site where you can download
            the latest version of this plugin.
        :rtype: str
        """
        return self.__website

    def __init__(self, plugin_id, descriptor_file, global_config):
        """
        Load a plugin descriptor file.

        :param plugin_id: Plugin ID.
        :type plugin_id: str

        :param descriptor_file: Descriptor file (with ".golismero" extension).
        :type descriptor_file: str

        :param global_config: Orchestrator settings.
        :type global_config: OrchestratorConfig
        """
        self.__plugin_id = plugin_id
        descriptor_file = path.abspath(descriptor_file)
        self.__descriptor_file = descriptor_file
        parser = RawConfigParser()
        parser.read(descriptor_file)
        try:
            plugin_module = parser.get('Core', 'Module')
        except Exception:
            plugin_module = path.splitext(path.basename(descriptor_file))[0]

        try:
            plugin_class = parser.get('Core', 'Class')
        except Exception:
            plugin_class = None

        try:
            stage = parser.get('Core', 'Stage')
        except Exception:
            stage = None

        try:
            dependencies = parser.get('Core', 'Dependencies')
        except Exception:
            dependencies = None

        try:
            recursive = parser.get('Core', 'Recursive')
        except Exception:
            recursive = 'no'

        if not stage:
            try:
                category, subcategory = plugin_id.split('/')[:2]
                category = category.strip().lower()
                subcategory = subcategory.strip().lower()
                if category == 'testing':
                    self.__stage_number = STAGES[subcategory]
                else:
                    self.__stage_number = 0
            except Exception:
                self.__stage_number = 0

        else:
            try:
                self.__stage_number = STAGES[stage.lower()]
            except KeyError:
                try:
                    self.__stage_number = int(stage)
                    if self.__stage_number not in STAGES.values():
                        raise ValueError()
                except Exception:
                    msg = 'Error parsing %r: invalid execution stage: %r'
                    raise ValueError(msg % (descriptor_file, stage))

            if not plugin_module.endswith('.py'):
                plugin_module += '.py'
            if path.sep != '/':
                plugin_module = plugin_module.replace('/', path.sep)
            if path.isabs(plugin_module):
                msg = 'Error parsing %r: plugin module path is absolute'
                raise ValueError(msg % descriptor_file)
            plugin_folder = path.split(descriptor_file)[0]
            plugin_module = path.abspath(path.join(plugin_folder, plugin_module))
            plugins_root = path.abspath(global_config.plugins_folder)
            if not plugins_root.endswith(path.sep):
                plugins_root += path.sep
            if not plugin_module.startswith(plugins_root):
                msg = 'Error parsing %r: plugin module (%s) is located outside the plugins folder (%s)' % (
                 descriptor_file, plugin_module, plugins_root)
                raise ValueError(msg)
            if plugin_class is not None:
                plugin_class = re.sub('\\W|^(?=\\d)', '_', plugin_class.strip())
                if iskeyword(plugin_class):
                    msg = 'Error parsing %r: plugin class (%s) is a Python reserved keyword' % (
                     plugin_class, descriptor_file)
                    raise ValueError(msg)
            self.__plugin_module = plugin_module
            self.__plugin_class = plugin_class
            if not dependencies:
                self.__dependencies = ()
            else:
                self.__dependencies = tuple(sorted({x.strip() for x in dependencies.split(',')}))
            try:
                self.__recursive = Configuration.boolean(recursive)
            except Exception:
                msg = 'Error parsing %r: invalid recursive flag: %r'
                raise ValueError(msg % (descriptor_file, recursive))

            try:
                self.__display_name = parser.get('Documentation', 'Name')
            except Exception:
                self.__display_name = plugin_id

            try:
                self.__description = parser.get('Documentation', 'Description')
            except Exception:
                self.__description = self.__display_name

            try:
                self.__version = parser.get('Documentation', 'Version')
            except Exception:
                self.__version = '?.?'

            try:
                self.__author = parser.get('Documentation', 'Author')
            except Exception:
                self.__author = 'Anonymous'

            try:
                self.__copyright = parser.get('Documentation', 'Copyright')
            except Exception:
                self.__copyright = 'No copyright information'

            try:
                self.__license = parser.get('Documentation', 'License')
            except Exception:
                self.__license = 'No license information'

            try:
                self.__website = parser.get('Documentation', 'Website')
            except Exception:
                self.__website = 'https://github.com/golismero'

            self.__plugin_passwd_args = set()
            self.__plugin_args = {}
            try:
                args = parser.items('Arguments')
            except Exception:
                args = ()

            for key, value in args:
                if key.startswith('*'):
                    key = key[1:].strip()
                    self.__plugin_passwd_args.add(key)
                self.__plugin_args[key] = value

            try:
                self.__plugin_config = dict(parser.items('Configuration'))
            except Exception:
                self.__plugin_config = dict()

            self.__plugin_extra_config = dict()
            for section in parser.sections():
                if section not in ('Core', 'Documentation', 'Configuration', 'Arguments'):
                    options = dict((k.lower(), v) for k, v in parser.items(section))
                    self.__plugin_extra_config[section] = options

        self.__read_config_file(global_config.config_file)
        self.__read_config_file(global_config.user_config_file)
        self.__read_config_file(global_config.profile_file)
        return

    def __copy__(self):
        raise NotImplementedError('Only deep copies, please!')

    def __deepcopy__(self):
        instance = EmptyNewStyleClass()
        instance.__class__ = self.__class__
        instance.__plugin_id = self.__plugin_id
        instance.__descriptor_file = self.__descriptor_file
        instance.__display_name = self.__display_name
        instance.__stage_number = self.__stage_number
        instance.__recursive = self.__recursive
        instance.__plugin_module = self.__plugin_module
        instance.__plugin_class = self.__plugin_class
        instance.__dependencies = self.__dependencies
        instance.__description = self.__description
        instance.__version = self.__version
        instance.__author = self.__author
        instance.__copyright = self.__copyright
        instance.__license = self.__license
        instance.__website = self.__website
        instance.__plugin_args = self.__plugin_args.copy()
        instance.__plugin_passwd_args = self.__plugin_passwd_args.copy()
        instance.__plugin_config = self.__plugin_config.copy()
        instance.__plugin_extra_config = {k:v.copy() for k, v in self.__plugin_extra_config.iteritems()}
        return instance

    def __repr__(self):
        return '<PluginInfo instance at %x: id=%s, stage=%s, recursive=%s, dependencies=%r, args=%r, config=%r, extra=%r>' % (
         id(self),
         self.plugin_id,
         self.stage,
         self.recursive,
         self.dependencies,
         self.plugin_args,
         self.plugin_config,
         self.plugin_extra_config)

    def to_dict(self):
        r"""
        Convert this PluginInfo object into a dictionary.

        :returns: Converted PluginInfo object.
        :rtype: dict(str -> \*)
        """
        return {'plugin_id': self.plugin_id, 
           'descriptor_file': self.descriptor_file, 
           'category': self.category, 
           'stage': self.stage, 
           'stage_number': self.stage_number, 
           'dependencies': self.dependencies, 
           'recursive': self.recursive, 
           'plugin_module': self.plugin_module, 
           'plugin_class': self.plugin_class, 
           'display_name': self.display_name, 
           'description': self.description, 
           'version': self.version, 
           'author': self.author, 
           'copyright': self.copyright, 
           'license': self.license, 
           'website': self.website, 
           'plugin_args': self.plugin_args.copy(), 
           'plugin_passwd_args': self.plugin_passwd_args.copy(), 
           'plugin_config': self.plugin_config.copy(), 
           'plugin_extra_config': {k:v.copy() for k, v in self.plugin_extra_config.iteritems()}}

    def customize_for_audit(self, audit_config):
        """
        Return a new PluginInfo instance with its configuration overriden
        by the audit settings.

        :param audit_config: Audit settings.
        :type audit_config: AuditConfig

        :returns: New, customized PluginInfo instance.
        :rtype: PluginInfo
        """
        if not isinstance(audit_config, AuditConfig):
            raise TypeError('Expected AuditConfig, got %r instead' % type(audit_config))
        new_instance = self.__deepcopy__()
        new_instance.__read_config_file(audit_config.config_file)
        new_instance.__read_config_file(audit_config.user_config_file)
        new_instance.__read_config_file(audit_config.profile_file)
        return new_instance

    def __read_config_file(self, config_file):
        """
        Private method to override plugin settings from a config file.

        :param config_file: Configuration file.
        :type config_file: str
        """
        if not config_file:
            return
        section_prefix = self.__plugin_id
        section_prefix_short = section_prefix[section_prefix.rfind('/') + 1:]
        config_parser = RawConfigParser()
        config_parser.read(config_file)
        for section in config_parser.sections():
            if section in (section_prefix, section_prefix_short):
                target = self.__plugin_args
            elif ':' in section:
                a, b = section.split(':', 1)
                a, b = a.strip(), b.strip()
                if a not in (section_prefix, section_prefix_short):
                    continue
                if b == 'Arguments':
                    target = self.__plugin_args
                elif b == 'Configuration':
                    target = self.__plugin_config
                elif b in ('Core', 'Documentation'):
                    msg = 'Ignored section [%s] of file %s'
                    warnings.warn(msg % (section, config_file))
                    continue
                else:
                    try:
                        target = self.__plugin_extra_config[b]
                    except KeyError:
                        target = self.__plugin_extra_config[b] = dict()

            else:
                continue
            target.update(config_parser.items(section))

    def _fix_classname(self, plugin_class):
        """
        Protected method to update the class name if found during plugin load.
        (Assumes it's always valid, so no sanitization is performed).

        .. warning: This method is called internally by GoLismero,
                    do not call it yourself!

        :param plugin_class: Plugin class name.
        :type plugin_class: str
        """
        self.__plugin_class = plugin_class


class PluginManager(object):
    """
    Plugin Manager.
    """
    min_stage = min(*STAGES.values())
    max_stage = max(*STAGES.values())
    assert sorted(STAGES.itervalues()) == range(min_stage, max_stage + 1)

    def __init__(self, orchestrator=None):
        """
        :param orchestrator: Orchestrator instance.
        :type orchestrator: Orchestrator
        """
        self.__orchestrator = orchestrator
        self.__plugins = {}
        self.__cache = {}

    @property
    def orchestrator(self):
        """
        :returns: Orchestrator instance.
        :rtype: Orchestrator
        """
        return self.__orchestrator

    @classmethod
    def get_stage_name_from_value(cls, value):
        """
        :param value: Stage value. See STAGES.
        :type value: int

        :returns: Stage name.
        :rtype: str

        :raise KeyError: Stage value not found.
        """
        for name, val in STAGES.iteritems():
            if value == val:
                return name

        raise KeyError('Stage value not found: %r' % value)

    def find_plugins(self, config):
        """
        Find plugins in the given folder.

        The folder must contain one subfolder for each plugin category,
        inside which are the plugins.

        Each plugin is defined in a file with the ".golismero" extension.
        The code for each plugin must be in a Python script within the same
        folder as the ".golismero" file, or within any subdirectory of it.

        :param config: Orchestrator or Audit settings.
        :type config: OrchestratorConfig | AuditConfig

        :returns: A list of plugins loaded,
            and a list of plugins that failed to load.
        :rtype: tuple(list(str), list(str))
        """
        if not isinstance(config, OrchestratorConfig):
            raise TypeError('Expected OrchestratorConfig, got %r instead' % type(config))
        plugins_folder = config.plugins_folder
        if plugins_folder:
            plugins_folder = path.abspath(plugins_folder)
        else:
            plugins_folder = get_default_plugins_folder()
        if not path.isdir(plugins_folder):
            raise ValueError('Invalid plugins folder: %s' % plugins_folder)
        if config.plugins_folder != plugins_folder:
            config.plugins_folder = plugins_folder
        success = list()
        failure = list()
        for current_category, _ in CATEGORIES.iteritems():
            category_folder = path.join(plugins_folder, current_category)
            if not path.isdir(category_folder):
                warnings.warn('Missing plugin category folder: %s' % category_folder)
                continue
            for dirpath, _, filenames in walk(category_folder):
                for fname in filenames:
                    if not fname.endswith('.golismero'):
                        continue
                    fname = path.abspath(path.join(dirpath, fname))
                    plugin_id = path.splitext(fname)[0][len(plugins_folder):]
                    if plugin_id[0] == path.sep:
                        plugin_id = plugin_id[1:]
                    if path.sep != '/':
                        plugin_id = plugin_id.replace(path.sep, '/')
                    if plugin_id in self.__plugins:
                        failure.append(plugin_id)
                        continue
                    try:
                        plugin_info = PluginInfo(plugin_id, fname, config)
                        self.__plugins[plugin_id] = plugin_info
                        success.append(plugin_id)
                    except Exception as e:
                        warnings.warn('Failure while loading plugins: %s' % e)
                        failure.append(plugin_id)

        return (
         success, failure)

    def get_plugins(self, category='all'):
        """
        Get info on the available plugins, optionally filtering by category.

        :param category: Category or stage.
            Use "all" to get plugins from all categories.
            Use "testing" to get all testing plugins for all stages.
        :type category: str

        :returns: Mapping of plugin IDs to instances of PluginInfo.
        :rtype: dict(str -> PluginInfo)

        :raises KeyError: The requested category or stage doesn't exist.
        """
        category = category.lower()
        if category == 'all':
            return self.__plugins.copy()
        if category in CATEGORIES:
            return {plugin_id:plugin_info for plugin_id, plugin_info in self.__plugins.iteritems() if plugin_info.category == category}
        if category in STAGES:
            stage_num = STAGES[category]
            return {plugin_id:plugin_info for plugin_id, plugin_info in self.__plugins.iteritems() if plugin_info.stage_number == stage_num}
        raise KeyError('Unknown plugin category or stage: %r' % category)

    def get_plugin_ids(self, category='all'):
        """
        Get the names of the available plugins,
        optionally filtering by category.

        :param category: Category or stage.
            Use "all" to get plugins from all categories.
            Use "testing" to get all testing plugins for all stages.
        :type category: str

        :returns: Plugin IDs.
        :rtype: set(str)

        :raises KeyError: The requested category or stage doesn't exist.
        """
        return set(self.get_plugins(category).iterkeys())

    def get_plugin_by_id(self, plugin_id):
        """
        Get info on the requested plugin.

        :param plugin_id: Plugin ID.
        :type plugin_id: str

        :returns: Plugin information.
        :rtype: PluginInfo

        :raises KeyError: The requested plugin doesn't exist.
        """
        try:
            return self.__plugins[plugin_id]
        except KeyError:
            raise KeyError('Plugin not found: %r' % plugin_id)

    __getitem__ = get_plugin_by_id

    def guess_plugin_by_id(self, plugin_id):
        """
        Get info on the requested plugin.

        :param plugin_id: Plugin ID.
        :type plugin_id: str

        :returns: Plugin information.
        :rtype: PluginInfo

        :raises KeyError: The requested plugin doesn't exist,
            or more than one plugin matches the request.
        """
        if any(c in plugin_id for c in '?*['):
            found = self.search_plugins_by_mask(plugin_id)
            if len(found) != 1:
                raise KeyError('Plugin not found: %s' % plugin_id)
            return found.popitem()[1]
        try:
            return self.get_plugin_by_id(plugin_id)
        except KeyError:
            found = self.search_plugins_by_id(plugin_id)
            if len(found) != 1:
                raise
            return found.popitem()[1]

    def search_plugins_by_id(self, search_string):
        """
        Try to match the search string against plugin IDs.

        :param search_string: Search string.
        :type search_string: str

        :returns: Mapping of plugin IDs to instances of PluginInfo.
        :rtype: dict(str -> PluginInfo)
        """
        return {plugin_id:plugin_info for plugin_id, plugin_info in self.__plugins.iteritems() if search_string == plugin_id[plugin_id.rfind('/') + 1:]}

    def search_plugins_by_mask(self, glob_mask):
        """
        Try to match the glob mask against plugin IDs.

        If the glob mask has a / then it applies to the whole path,
        if it doesn't then it applies to either the whole path or
        a single component of it.

        :param glob_mask: Glob mask.
        :type glob_mask: str

        :returns: Mapping of plugin IDs to instances of PluginInfo.
        :rtype: dict(str -> PluginInfo)
        """
        gfilter = fnmatch.filter
        gmatch = fnmatch.fnmatch
        plugins = self.__plugins
        matches = {plugin_id:plugins[plugin_id] for plugin_id in gfilter(plugins.iterkeys(), glob_mask)}
        if '/' not in glob_mask:
            matches.update({plugin_id:plugin_info for plugin_id, plugin_info in plugins.iteritems() if any(gmatch(token, glob_mask) for token in plugin_id.split('/'))})
        return matches

    def search_plugins(self, search_string):
        """
        Try to match the search string against plugin IDs.
        The search string may be any substring or a glob mask.

        :param search_string: Search string.
        :type search_string: str

        :returns: Mapping of plugin IDs to instances of PluginInfo.
        :rtype: dict(str -> PluginInfo)
        """
        if any(c in search_string for c in '?*['):
            return self.search_plugins_by_mask(search_string)
        return self.search_plugins_by_id(search_string)

    def load_plugins(self, category='all'):
        """
        Get info on the available plugins, optionally filtering by category.

        :param category: Category or stage.
            Use "all" to get plugins from all categories.
            Use "testing" to get all testing plugins for all stages.
        :type category: str

        :returns: Mapping of plugin IDs to Plugin instances.
        :rtype: dict(str -> Plugin)

        :raises KeyError: The requested category or stage doesn't exist.
        :raises Exception: Plugins may throw exceptions if they fail to load.
        """
        return {name:self.load_plugin_by_id(name) for name in sorted(self.get_plugin_ids(category))}

    def load_plugin_by_id(self, plugin_id):
        """
        Load the requested plugin by ID.

        :param plugin_id: ID of the plugin to load.
        :type plugin_id: str

        :returns: Plugin instance.
        :rtype: Plugin

        :raises Exception: Plugins may throw exceptions if they fail to load.
        """
        instance = self.__cache.get(plugin_id, None)
        if instance is not None:
            return instance
        else:
            try:
                info = self.__plugins[plugin_id]
            except KeyError:
                raise KeyError('Plugin not found: %r' % plugin_id)

            clazz = load_plugin_class_from_info(info)
            if not info.plugin_class:
                info._fix_classname(clazz.__name__)
            instance = clazz()
            self.__cache[plugin_id] = instance
            return instance

    def get_plugin_info_from_instance(self, instance):
        """
        Get a plugin's name and information from its already loaded instance.

        :param instance: Plugin instance.
        :type instance: Plugin

        :returns: tuple(str, PluginInfo) -- Plugin ID and information.
        :raises KeyError: Plugin instance not found.
        """
        for name, value in self.__cache.iteritems():
            if value is instance:
                return (name, self.__plugins[name])

        try:
            r = repr(instance)
        except Exception:
            r = repr(id(instance))

        raise KeyError('Plugin instance not found: ' + r)

    def set_plugin_args(self, plugin_id, plugin_args):
        """
        Set the user-defined values for the given plugin arguments.

        :param plugin_id: Plugin ID.
        :type plugin_id: str

        :param plugin_args: Plugin arguments and their user-defined values.
        :type plugin_args: dict(str -> str)

        :returns: One of the following values:
             - 0: All values set successfully.
             - 1: The plugin was not loaded or does not exist.
             - 2: Some values were not defined for this plugin.
        """
        try:
            plugin_info = self.get_plugin_by_id(plugin_id)
        except KeyError:
            return 1

        target_args = plugin_info.plugin_args
        status = 0
        for key, value in plugin_args.iteritems():
            if key in target_args:
                target_args[key] = value
            else:
                status = 2

        return status

    def get_plugin_manager_for_audit(self, audit):
        """
        Instance an audit-specific plugin manager.

        :param audit: Audit.
        :type audit: Audit

        :returns: Plugin manager for this audit.
        :rtype: AuditPluginManager

        :raises ValueError: Configuration error.
        """
        return AuditPluginManager(self, audit.orchestrator.config, audit.config)

    def close(self):
        """
        Release all resources held by this manager.
        """
        self.__orchestrator = None
        self.__plugins = None
        self.__cache = None
        return


class AuditPluginManager(PluginManager):
    """
    Plugin manager for audits.
    """

    def __init__(self, pluginManager, orchestratorConfig, auditConfig):
        super(AuditPluginManager, self).__init__(pluginManager.orchestrator)
        self.__pluginManager = pluginManager
        self.__batches = None
        self.__stages = None
        self._PluginManager__plugins = self.__apply_config(auditConfig)
        return

    def initialize(self, audit_config):
        """
        Initializes the plugin arguments and disables the plugins that fail the
        parameter checks. Also calculates the dependencies.
        """
        if audit_config.plugin_args:
            for plugin_id, plugin_args in audit_config.plugin_args.iteritems():
                status = self.set_plugin_args(plugin_id, plugin_args)
                if status == 1:
                    try:
                        self.__pluginManager.get_plugin_by_id(plugin_id)
                    except KeyError:
                        warnings.warn('Unknown plugin ID: %s' % plugin_id, RuntimeWarning)

                elif status == 2:
                    warnings.warn('Some arguments undefined for plugin ID: %s' % plugin_id, RuntimeWarning)

        self.__check_plugin_params(audit_config)
        self.__calculate_dependencies()

    @property
    def pluginManager(self):
        """
        :returns: Plugin manager.
        :rtype: PluginManager
        """
        return self.__pluginManager

    @property
    def batches(self):
        """
        :returns: Plugin execution batches.
        :rtype: list(set(str))
        """
        return self.__batches

    @property
    def stages(self):
        """
        :returns: Mapping of stage names to plugin IDs for each stage.
        :rtype: dict(str -> set(str))
        """
        return self.__stages

    def __apply_config(self, auditConfig):
        """
        Apply the black and white lists.
        This controls which plugins are loaded and which aren't.

        :param auditConfig: Audit configuration.
        :type auditConfig: AuditConfig

        :returns: Mapping of the approved plugin IDs to
                  reconfigured instances of PluginInfo.
        :rtype: dict(str -> PluginInfo)

        :raises ValueError: Configuration error.
        :raises KeyError: Configuration error.
        """
        if not isinstance(auditConfig, AuditConfig):
            raise TypeError('Expected AuditConfig, got %r instead' % type(auditConfig))
        enable_plugins = auditConfig.enable_plugins
        disable_plugins = auditConfig.disable_plugins
        plugin_load_overrides = auditConfig.plugin_load_overrides
        if not enable_plugins and not disable_plugins and not plugin_load_overrides:
            raise ValueError('No plugins selected for audit!')
        all_plugins = self.pluginManager.get_plugin_ids()
        if not all_plugins:
            raise SyntaxError('Internal error!')
        blacklist_approach = False
        if 'all' in enable_plugins:
            enable_plugins = {
             'all'}
        if 'all' in disable_plugins:
            disable_plugins = {
             'all'}
            blacklist_approach = True
        enable_plugins = set(enable_plugins)
        disable_plugins = set(disable_plugins)
        conflicting_entries = enable_plugins.intersection(disable_plugins)
        if conflicting_entries:
            if len(conflicting_entries) > 1:
                msg = 'The same entries are present in both black and white lists: %s' % (', ').join(conflicting_entries)
            else:
                msg = 'The same entry (%s) is present in both black and white lists' % conflicting_entries.pop()
            raise ValueError(msg)
        disable_plugins = self.__expand_plugin_list(disable_plugins, 'blacklist')
        enable_plugins = self.__expand_plugin_list(enable_plugins, 'whitelist')
        if blacklist_approach:
            plugins = all_plugins.intersection(enable_plugins)
        else:
            plugins = all_plugins.difference(disable_plugins)
        if plugin_load_overrides:
            only_enables = all(x[0] for x in plugin_load_overrides)
            overrides = []
            if only_enables:
                plugin_load_overrides.insert(0, (False, 'all'))
            for flag, token in plugin_load_overrides:
                token = token.strip().lower()
                if token in ('all', 'testing'):
                    names = self.pluginManager.get_plugin_ids('testing')
                    overrides.append((flag, names))
                elif token in STAGES:
                    names = self.pluginManager.get_plugin_ids(token)
                    overrides.append((flag, names))
                elif token in all_plugins:
                    info = self.pluginManager.get_plugin_by_id(token)
                    if info.category != 'testing':
                        raise ValueError('Not a testing plugin: %s' % token)
                    overrides.append((flag, (token,)))
                elif any(c in token for c in '?*['):
                    matching_plugins = self.pluginManager.search_plugins_by_mask(token)
                    for name, info in matching_plugins.iteritems():
                        if info.category != 'testing':
                            raise ValueError('Not a testing plugin: %s' % token)
                        overrides.append((flag, (name,)))

                else:
                    matching_plugins = self.pluginManager.search_plugins_by_id(token)
                    if not matching_plugins:
                        raise ValueError('Unknown plugin: %s' % token)
                    if len(matching_plugins) > 1:
                        msg = 'Ambiguous plugin ID %r may refer to any of the following plugins: %s' % (
                         token,
                         (', ').join(sorted(matching_plugins.iterkeys())))
                        raise ValueError(msg)
                    name, info = matching_plugins.items()[0]
                    if info.category != 'testing':
                        raise ValueError('Not a testing plugin: %s' % token)
                    overrides.append((flag, (name,)))

            for enable, names in overrides:
                if enable:
                    plugins.update(names)
                else:
                    plugins.difference_update(names)

        plugins.update(self.pluginManager.get_plugin_ids('ui'))
        return {name:self.pluginManager[name].customize_for_audit(auditConfig) for name in plugins}

    def __expand_plugin_list(self, plugin_list, list_name):
        """
        Expand aliases in a plugin black/white list.

        :param plugin_list: Plugin black/white list.
        :type plugin_list: set

        :param list_name: Name of the list ("blacklist" or "whitelist").
        :type list_name: str

        :returns: Black/white list with expanded aliases.
        :rtype: set

        :raises ValueError: Configuration error.
        :raises KeyError: Configuration error.
        """
        if 'all' in plugin_list:
            plugin_list = self.pluginManager.get_plugin_ids()
        else:
            for category in CATEGORIES:
                if category in plugin_list:
                    plugin_list.remove(category)
                    plugin_list.update(self.pluginManager.get_plugin_ids(category))

            for stage in STAGES:
                if stage in plugin_list:
                    plugin_list.remove(stage)
                    plugin_list.update(self.pluginManager.get_plugin_ids(stage))

            missing_plugins = set()
            all_plugins = self.pluginManager.get_plugin_ids()
            for plugin_id in sorted(plugin_list):
                if plugin_id not in all_plugins:
                    matching_plugins = set(self.pluginManager.search_plugins(plugin_id).keys())
                    if not matching_plugins:
                        missing_plugins.add(plugin_id)
                        continue
                    if len(matching_plugins) > 1 and '*' not in plugin_id:
                        msg = 'Ambiguous entry in %s (%r) may refer to any of the following plugins: %s'
                        msg %= (list_name,
                         plugin_id, (', ').join(sorted(matching_plugins)))
                        raise ValueError(msg)
                    plugin_list.remove(plugin_id)
                    plugin_list.update(matching_plugins)

        if missing_plugins:
            if len(missing_plugins) > 1:
                msg = 'Unknown plugins in %s: %s'
                msg %= (list_name, (', ').join(sorted(missing_plugins)))
            else:
                msg = 'Unknown plugin in %s: %s'
                msg %= (list_name, missing_plugins.pop())
            raise KeyError(msg)
        return plugin_list

    def __calculate_dependencies(self):
        """
        Generate a dependency graph for all plugins found, and calculate
        the batches of plugins that can be run concurrently.

        :raises ValueError: The dependencies are broken.
        """
        plugins = self.get_plugins('testing')
        all_plugins = set(plugins.iterkeys())
        graph = defaultdict(set)
        stages = defaultdict(set)
        for plugin_id, info in plugins.iteritems():
            stage = info.stage_number
            if not stage or stage < 0:
                stage = 0
            stages[stage].add(plugin_id)
            deps = set(info.dependencies)
            if not deps.issubset(all_plugins):
                msg = 'Plugin %s depends on missing plugin(s): %s'
                msg %= (plugin_id,
                 (', ').join(sorted(deps.difference(all_plugins))))
                raise ValueError(msg)
            graph[plugin_id] = deps

        stage_numbers = sorted(STAGES.itervalues())
        for n in stage_numbers:
            this_stage = '* stage %d' % n
            next_stage = '* stage %d' % (n + 1)
            graph[next_stage].add(this_stage)

        for n in stage_numbers:
            bridge = '* stage %d' % n
            graph[bridge].update(stages[n])
            for node in stages[(n + 1)]:
                graph[node].add(bridge)

        batches = []
        while graph:
            ready = {plugin_id for plugin_id, deps in graph.iteritems() if not deps if not deps}
            if not ready:
                msg = 'Circular dependencies found in plugins: '
                keys = [ k for k in graph.iterkeys() if not k.startswith('*')
                       ]
                keys.sort()
                raise ValueError(msg + (', ').join(keys))
            for plugin_id in ready:
                del graph[plugin_id]

            for deps in graph.itervalues():
                deps.difference_update(ready)

            ready = {k for k in ready if not k.startswith('*') if not k.startswith('*')}
            if ready:
                batches.append(ready)

        self.__batches = batches
        self.__stages = stages

    def __check_plugin_params(self, audit_config):
        """
        Check the plugin parameters.
        Plugins that fail this check are automatically disabled.
        """
        orchestrator = self.orchestrator
        plugins = self.get_plugins('testing')
        for plugin_id in plugins:
            plugin = self.load_plugin_by_id(plugin_id)
            new_ctx = orchestrator.build_plugin_context(None, plugin, None)
            new_ctx = PluginContext(orchestrator_pid=new_ctx._orchestrator_pid, orchestrator_tid=new_ctx._orchestrator_tid, msg_queue=new_ctx.msg_queue, ack_identity=None, plugin_info=self.get_plugin_by_id(plugin_id), audit_name=audit_config.audit_name, audit_config=audit_config, audit_scope=new_ctx.audit_scope)
            old_ctx = Config._context
            try:
                Config._context = new_ctx
                try:
                    plugin.check_params()
                except Exception as e:
                    del self._PluginManager__plugins[plugin_id]
                    err_tb = traceback.format_exc()
                    err_msg = 'Plugin disabled, reason: %s' % str(e)
                    Logger.log_error_verbose(err_msg)
                    Logger.log_error_more_verbose(err_tb)

            finally:
                Config._context = old_ctx

        return

    def next_concurrent_plugins(self, candidate_plugins):
        """
        Based on the previously executed plugins, get the next plugins
        to execute.

        :param candidate_plugins: Plugins we may want to execute.
        :type candidate_plugins: set(str)

        :returns: Next plugins to execute.
        :rtype: set(str)
        """
        if candidate_plugins:
            for batch in self.__batches:
                batch = batch.intersection(candidate_plugins)
                if batch:
                    return batch

        return set()

    def find_plugins(self, plugins_folder=None):
        """
        .. warning: This method is not available for audits.
        """
        raise NotImplementedError('Not available for audits!')

    def get_plugin_manager_for_audit(self, audit):
        """
        .. warning: This method is not available for audits.
        """
        raise NotImplementedError('Not available for audits!')

    def load_plugin_by_id(self, plugin_id):
        info = self.get_plugin_by_id(plugin_id)
        instance = self.pluginManager.load_plugin_by_id(plugin_id)
        info._fix_classname(instance.__class__.__name__)
        return instance

    def get_plugin_info_from_instance(self, instance):
        plugin_id, info = self.pluginManager.get_plugin_info_from_instance(instance)
        try:
            return (
             plugin_id, self.get_plugin_by_id(plugin_id))
        except KeyError:
            return (
             plugin_id, info)

    def close(self):
        try:
            super(AuditPluginManager, self).close()
        finally:
            self.__pluginManager = None
            self.__batches = None
            self.__stages = None

        return