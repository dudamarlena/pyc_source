# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/ConfigGenerator.py
# Compiled at: 2015-08-17 15:21:11
from configmaster.ConfigFile import ConfigFile, NetworkedConfigObject

def GenerateConfigFile(load_hook, dump_hook, **kwargs) -> ConfigFile:
    """
    Generates a ConfigFile object using the specified hooks.

    These hooks should be functions, and have one argument.
    When a hook is called, the ConfigFile object is passed to it. Use this to load your data from the fd object, or request, or whatever.

    This returns a ConfigFile object.
    """

    def ConfigFileGenerator(filename, safe_load: bool=True):
        cfg = ConfigFile(fd=filename, load_hook=load_hook, dump_hook=dump_hook, safe_load=safe_load, **kwargs)
        return cfg

    return ConfigFileGenerator


def GenerateNetworkedConfigFile(load_hook, normal_class_load_hook, normal_class_dump_hook, **kwargs) -> NetworkedConfigObject:
    """
    Generates a NetworkedConfigObject using the specified hooks.
    """

    def NetworkedConfigObjectGenerator(url, safe_load: bool=True):
        cfg = NetworkedConfigObject(url=url, load_hook=load_hook, safe_load=safe_load, normal_class_load_hook=normal_class_load_hook, normal_class_dump_hook=normal_class_dump_hook)
        return cfg

    return NetworkedConfigObjectGenerator