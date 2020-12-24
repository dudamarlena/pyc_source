# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\tools\defaults.py
# Compiled at: 2009-01-15 21:25:08
""" Defaults
    Provides default configuration interface
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: defaults.py 809 2009-01-16 02:27:11Z JeanLou.Dupont $'
import yaml, os, sys, logging, jld.api as api

class Defaults(object):
    """
    """
    _path = None

    def __init__(self, filepath=None):
        self.filepath = filepath
        self.defaults = None
        self._load()
        return

    def _load(self):
        path = self.filepath if self.filepath else self._path
        try:
            file = open(path, 'r')
            self.defaults = yaml.load(file)
            file.close()
        except Exception, e:
            raise api.ErrorConfig('error_load_file', {'path': path})