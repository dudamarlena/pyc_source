# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maciejczyzewski/teax/repository/teax/config.py
# Compiled at: 2016-02-02 14:28:54
"""teax configuration parser"""
import os
from teax import tty
from teax.messages import T_CONF_FILE_FAILURE
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class ConfigObject(object):
    """
    Class which holds the configuration values.

        >>> conf = ConfigObject('my_config.ini')
        >>> print conf['book']
        {u'author': u'MAC'}
        >>> conf['book.author'] = 'OMG'
        >>> conf['book.test'] = {'a': 1234, 'b': 4321}
        >>> print conf['book']
        {'test': {'a': 1234, 'b': 4321}, u'author': u'OMG'}
        >>> conf.load()
        >>> print conf['book']
        {'test': {'a': 1234, 'b': 4321}, u'author': u'MAC'}

    All values used in command-line interface should be here.
    """
    STORAGE = {}
    FILENAME = ''
    _INSTANCE = None

    def __init__(self, filename='teax.ini'):
        self.load(filename)

    def load(self, filename=''):
        """ Loads configuration file. """
        if os.path.isfile(filename):
            self.FILENAME = filename
            self._load_instance()
        if self._INSTANCE:
            _variables = self._convert_to_dict(self._INSTANCE)
            self.STORAGE = self._merge_dicts(self.STORAGE, _variables)

    def save(self, filename, keys):
        cfgfile = open(filename, 'w')
        if not self._INSTANCE:
            self._INSTANCE = configparser.ConfigParser()
        for key in keys:
            section, keyword = self._parse_address(key)
            if section not in self._INSTANCE.sections():
                self._INSTANCE.add_section(section)
            self._INSTANCE.set(section, keyword, self.__getitem__(key))

        self._INSTANCE.write(cfgfile)
        cfgfile.close()

    def __getitem__(self, key):
        level = len(self._parse_address(key))
        if level == 2:
            section, keyword = self._parse_address(key)
            if section in self.STORAGE and keyword in self.STORAGE[section]:
                return self.STORAGE[section][keyword]
            return
        if level == 1:
            if key in self.STORAGE:
                return self.STORAGE[key]
            return
        return self.STORAGE
        return

    def __setitem__(self, key, value):
        section, keyword = self._parse_address(key)
        if section not in self.STORAGE:
            self.STORAGE[section] = {}
        self.STORAGE[section][keyword] = value

    def _load_instance(self):
        try:
            self._INSTANCE = configparser.ConfigParser()
            self._INSTANCE.read(self.FILENAME)
        except:
            tty.warning(T_CONF_FILE_FAILURE)

    def _convert_to_dict(self, instance, _dict={}):
        for section in instance.sections():
            _dict[section] = {}
            for key, val in instance.items(section):
                _dict[section][key] = val

        return _dict

    def _merge_dicts(self, left, right, path=[]):
        for key in right:
            if key in left and isinstance(left[key], dict) and isinstance(right[key], dict):
                self._merge_dicts(left[key], right[key], path + [str(key)])
            else:
                left[key] = right[key]

        return left

    def _parse_address(self, string):
        if not string:
            return []
        return string.split('.')