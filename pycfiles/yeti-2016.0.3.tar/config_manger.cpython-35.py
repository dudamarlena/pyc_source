# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/PycharmProjects/Yeti/yeti/config_manger.py
# Compiled at: 2015-10-06 10:01:46
# Size of source mod 2**32: 4197 bytes
import logging
from .module_loader import ModuleLoader
logger = logging.getLogger('yeti.ConfigManager')

class ConfigurationError(Exception):
    pass


class ConfigManager(object):
    __doc__ = '\n    Uses instances of :class:`ModuleLoader` to load modules from reference lists in a configuration file.\n    '
    _STARTUP_MOD_SECTION = 'StartupMods'
    _config_path = ''

    def __init__(self):
        self.config_structure = None
        self.module_loaders = dict()

    def load_startup_mods(self, context):
        """
        Find all modules in the "StartupMods" section of the config file, and load them with instances of :class:`ModuleLoader`
        into the specified context.

        :param context: The context to load the modules into.
        """
        if self.config_structure is None:
            raise ConfigurationError('No config file loaded.')
        for module_name in self.config_structure[self._STARTUP_MOD_SECTION]:
            self.load_module(module_name, context)

    def load_module(self, name, context):
        """
        This uses a loaded config file to generate a fallback list and use a :class:`ModuleLoader` to load the module.

        :param name: The name reference of the module to load.
        :param context: The context to load the module into.

        :returns: The created :class:`ModuleLoader`
        """
        context.config_manager = self
        if self.config_structure is None:
            fallback_list = [
             name]
            fallback_index = 0
        else:
            if name in self.config_structure:
                fallback_list = self.config_structure[name]
                fallback_index = 0
            else:
                for subsystem_config in self.config_structure:
                    if subsystem_config != self._STARTUP_MOD_SECTION and name in self.config_structure[subsystem_config]:
                        fallback_list = self.config_structure[subsystem_config]
                        fallback_index = fallback_list.index(name)
                        break
                else:
                    fallback_list = [
                     name]
                    fallback_index = 0

        module_loader = ModuleLoader()
        module_loader.set_context(context)
        module_loader.fallback_list = fallback_list
        module_loader.fallback_index = fallback_index
        module_loader.load()
        self.module_loaders[name] = module_loader
        return module_loader

    def parse_config(self, path):
        """
        Parse the config file.

        :param path: The file path of the config file to parse.

        :returns: The dictionary of the parsed config file.
        """
        if path == '':
            path = self._config_path
        self._config_path = path
        f = open(path)
        section = None
        parsed_config = dict()
        for line in f:
            line = line.rstrip('\r\n')
            if '#' in line:
                line, comment = line.split('#', 1)
                line = line.strip()
            if '[' in line:
                section = line.split('[', 1)[1].split(']', 1)[0]
                parsed_config[section] = list()
            elif line is not '':
                parsed_config[section].append(line)

        logger.info('Finished parsing ' + path)
        self.config_structure = parsed_config
        return parsed_config