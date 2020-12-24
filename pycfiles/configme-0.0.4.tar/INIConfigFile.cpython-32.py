# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/INIConfigFile.py
# Compiled at: 2015-09-06 05:02:18
import configparser
from configmaster import exc
from configmaster.ConfigGenerator import GenerateConfigFile

def ini_load_hook(cfg, **kwargs):
    """
    This handles automatically opening/creating the INI configuration files.

    >>> import configmaster.INIConfigFile
    >>> cfg = configmaster.INIConfigFile.INIConfigFile("tesr.ini") # Accepts a string for input

    >>> fd = open("test.ini") # Accepts a file descriptor too
    >>> cfg2 = configmaster.INIConfigFile.INIConfigFile(fd)

    ConfigMaster objects accepts either a string for the relative path of the INI file to load, or a :io.TextIOBase: object to read from.
    If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

    To access config objects programmatically, a config object is exposed via the use of cfg.config.
    These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.
    """
    cfg.tmpini = configparser.ConfigParser()
    try:
        cfg.tmpini.read_file(cfg.fd)
    except ValueError as e:
        raise exc.LoaderException('Could not decode INI file: {}'.format(e)) from e

    tmpdict = {}
    for name in cfg.tmpini.sections():
        data = dict(cfg.tmpini[name])
        tmpdict[name] = data

    cfg.config.load_from_dict(tmpdict)


def ini_dump_hook(cfg, text: bool=False):
    """
    Dumps all the data into a INI file.

    This will automatically kill anything with a '_' in the keyname, replacing it with a dot. You have been warned.
    """
    data = cfg.config.dump()
    ndict = {}
    for key, item in data.items():
        key = key.replace('_', '.')
        ndict[key] = item

    cfg.tmpini = configparser.ConfigParser()
    cfg.tmpini.read_dict(data)
    if not text:
        cfg.tmpini.write(cfg.fd)
    else:
        return
    cfg.reload()


INIConfigFile = GenerateConfigFile(load_hook=ini_load_hook, dump_hook=ini_dump_hook)