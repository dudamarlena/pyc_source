# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/loaders/json.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 1053 bytes
"""Loader for JSON format files."""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import json
from . import base

class JsonFile(base.ConfigurationFile):
    __doc__ = 'Configuration file parser for JSON style files.'

    def __init__(self, *args, **kwargs):
        super(JsonFile, self).__init__(*args, **kwargs)
        self._parsed = None

    @property
    def parsed(self):
        """Get the JSON dictionary object which represents the content.

        This property is cached and only parses the content once.
        """
        if not self._parsed:
            self._parsed = json.loads(self.content)
        return self._parsed

    @property
    def namespaces(self):
        """Get an iterable of str representing namespaces within the config."""
        return self.parsed.keys()

    def items(self, namespace):
        """Get a dictionary of entries under a given namespace."""
        return self.parsed.copy().get(namespace, {})