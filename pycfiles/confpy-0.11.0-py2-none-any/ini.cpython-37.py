# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/loaders/ini.py
# Compiled at: 2019-08-24 22:16:44
# Size of source mod 2**32: 1136 bytes
"""Loader for INI format files."""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import io
from . import base
from core.compat import ConfigParser

class IniFile(base.ConfigurationFile):
    __doc__ = 'Configuration file parser for INI style files.'

    def __init__(self, *args, **kwargs):
        (super(IniFile, self).__init__)(*args, **kwargs)
        self._parsed = None

    @property
    def parsed(self):
        """Get the ConfigParser object which represents the content.

        This property is cached and only parses the content once.
        """
        if not self._parsed:
            self._parsed = ConfigParser()
            self._parsed.read_file(io.StringIO(self.content))
        return self._parsed

    @property
    def namespaces(self):
        """Get an iterable of str representing namespaces within the config."""
        return self.parsed.sections()

    def items(self, namespace):
        """Get a dictionary of entries under a given namespace."""
        return dict(self.parsed.items(namespace))