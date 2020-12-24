# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/common/settings.py
# Compiled at: 2016-12-05 02:21:59
# Size of source mod 2**32: 2949 bytes
"""
Contains functionality for reading settings from ini- and json-files

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
import configparser, os, json

class INISettings(object):
    __doc__ = 'This class is responsible for reading settings from ini-files and holding them in memory.'
    parser = None
    filename = None
    dirname = None

    def reload(self, _filename):
        """Reload all information"""
        self.parser.read(_filename)
        self.filename = _filename
        self.dirname = os.path.dirname(_filename)

    def handle_path(self, _path):
        if os.path.isabs(_path):
            return _path
        else:
            if _path[0] == '~':
                return os.path.expanduser(_path)
            return os.path.join(self.dirname, _path)

    def get(self, _section, _option, _default=None):
        """Get a certain option"""
        if self.parser.has_section(_section):
            if not self.parser.has_option(_section, _option):
                return _default
            else:
                return self.parser.get(_section, _option)
        else:
            return _default

    def get_path(self, _section, _option, _default=None):
        return self.handle_path(self.get(_section, _option, _default))

    def __init__(self, _filename=None):
        """Constructor"""
        if _filename:
            self.filename = _filename
            self.reload(_filename)


class JSONXPath(object):
    __doc__ = 'This class is responsible for reading settings from json-files and holding them in memory.'
    filename = None
    dirname = None
    data = None

    def reload(self, _filename):
        """Reload all information"""
        with open(_filename, 'r') as (f):
            self.data = json.load(f)
        self.filename = _filename
        self.dirname = os.path.dirname(_filename)

    def find(self, _xpath):
        _parts = _xpath.split('/')
        _curr_node = self.data
        for _curr_part in _parts:
            if _curr_part in _curr_node:
                _curr_node = _curr_node[_curr_part]
            else:
                return

        return _curr_node

    def handle_path(self, _path):
        if os.path.isabs(_path):
            return _path
        else:
            if _path[0] == '~':
                return os.path.expanduser(_path)
            return os.path.join(self.dirname, _path)

    def get(self, _xpath, _default=None):
        """Get a certain option"""
        _node = self.find(_xpath)
        if _node is not None:
            return _node
        else:
            return _default

    def get_path(self, _xpath, _default=None):
        return self.handle_path(self.get(_xpath, _default))

    def __init__(self, _filename=None):
        """Constructor"""
        if _filename:
            self.filename = _filename
            self.reload(_filename)