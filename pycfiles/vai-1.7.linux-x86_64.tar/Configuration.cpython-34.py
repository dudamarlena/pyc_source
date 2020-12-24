# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/Configuration.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2141 bytes
import copy, os, json, locale
from .. import paths

class Configuration:
    DEFAULTS = {'colors.syntax_schema': 'default', 
     'colors.status_bar.fg': 'yellow', 
     'colors.status_bar.bg': 'blue', 
     'colors.side_ruler.fg': 'cyan', 
     'colors.side_ruler.bg': 'transparent', 
     'icons.collection': 'unicode1'}
    _instance = None
    _filename = None
    flags = {'has_wide_ncurses': True}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def setFilename(cls, filename):
        if cls._instance is not None:
            if self._filename is not None:
                raise Exception('Configuration already initialized')
        cls._filename = filename

    @classmethod
    def filename(cls):
        if cls._filename is None:
            cls._filename = paths.configFile()
        return cls._filename

    @classmethod
    def save(cls):
        config = cls.instance()
        with open(cls._filename, 'w') as (f):
            f.write(json.dumps(config._config_dict, indent=4, sort_keys=True))

    def __init__(self):
        cls = self.__class__
        filename = cls.filename()
        try:
            with open(filename, 'r') as (f):
                merge_data = json.loads(f.read())
        except:
            merge_data = {}

        self._config_dict = copy.deepcopy(Configuration.DEFAULTS)
        self._config_dict.update(merge_data)

    def __getitem__(self, key):
        return self._config_dict[key]

    @classmethod
    def get(cls, key):
        if key == 'icons.collection' and locale.getpreferredencoding(False) != 'UTF-8' or not cls.flags.get('has_wide_ncurses'):
            return 'ascii'
        return cls.instance()[key]