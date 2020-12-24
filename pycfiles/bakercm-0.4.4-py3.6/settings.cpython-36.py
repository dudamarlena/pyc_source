# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\baker\settings.py
# Compiled at: 2018-11-12 14:30:20
# Size of source mod 2**32: 3738 bytes
from configparser import ConfigParser
from pathlib import Path
from baker.storage import Storage
_HOME_PATH = str(Path.home())
_BAKER_PATH = _HOME_PATH + '/.baker'
_BAKERC_PATH = _HOME_PATH + '/.bakerc'
_default_values = {'DEBUG':False, 
 'ENCODING':'utf-8', 
 'RECIPE_CASE_SENSITIVE':False, 
 'REPOSITORY':None, 
 'REPOSITORY_TYPE':None, 
 'REPOSITORY_AUTH':None, 
 'REPOSITORY_CUSTOM_PATTERN':None, 
 'STORAGE_RECIPE':_BAKER_PATH + '/recipes/', 
 'STORAGE_RECIPE_INDEX':_BAKER_PATH + '/index', 
 'STORAGE_RECIPE_META':_BAKER_PATH + '/meta', 
 'STORAGE_KEY_PATH':_BAKER_PATH + '/baker.key', 
 'STORAGE_TEMPLATES':_BAKER_PATH + '/templates/', 
 'TEMPLATE_EXT':'tpl'}

def get(key):
    """
    Get setting value from kwy
    """
    return values()[key]


def load(**kwargs):
    """
    Initial load of settings for running
    """
    global BAKER_SETTINGS
    BAKER_SETTINGS = _default_values
    _load_bakerc()
    for key, value in kwargs.items():
        values()[key] = value


def values(custom_only=False):
    """
    List of settings custom and defaults
    """
    if custom_only and Path(_BAKERC_PATH).is_file():
        lines = Storage.file(_BAKERC_PATH).split('\n')
        configs = {}
        for line in lines:
            if line:
                key, val = line.split('=')
                configs[key] = val

        return configs
    else:
        return globals()['BAKER_SETTINGS']


def _load_bakerc():
    """
    Load settings from bakerc file
    """

    def convert_if_bool(string):
        lower_str = string.lower()
        if lower_str in ('true', 'false'):
            return lower_str == 'true'
        else:
            return string

    if Path(_BAKERC_PATH).is_file():
        parser = ConfigParser()
        Storage.parser(_BAKERC_PATH, parser, chain_items=('[DEFAULT]', ))
        for key, value in parser.defaults().items():
            upper_key = key.upper()
            if upper_key not in values():
                raise AttributeError("Setting '{0}' at '{1}' is not supported".format(upper_key, _BAKERC_PATH))
            values()[upper_key] = convert_if_bool(value)