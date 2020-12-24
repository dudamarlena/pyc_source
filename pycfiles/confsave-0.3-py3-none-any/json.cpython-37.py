# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/loaders/json.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 1053 bytes
__doc__ = 'Loader for JSON format files.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import json
from . import base

class JsonFile(base.ConfigurationFile):
    """JsonFile"""

    def __init__(self, *args, **kwargs):
        (super(JsonFile, self).__init__)(*args, **kwargs)
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