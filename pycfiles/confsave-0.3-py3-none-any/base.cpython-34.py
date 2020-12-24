# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/loaders/base.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 2602 bytes
__doc__ = 'Base classes for all config file formats.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import os
from .. import exc
from ..core import compat
from ..core import config

class ConfigurationFile(object):
    """ConfigurationFile"""

    def __init__(self, path, strict=True):
        self._path = path
        self._content = None
        self._strict = strict

    @property
    def path(self):
        """Get the file path given at initialization."""
        return self._path

    @property
    def abspath(self):
        """Get the absolute path to the file."""
        return os.path.abspath(self._path)

    @property
    def content(self):
        """Get the file contents.

        This property is cached. The file is only read once.
        """
        if not self._content:
            self._content = self._read()
        return self._content

    @property
    def config(self):
        """Get a Configuration object from the file contents."""
        conf = config.Configuration()
        for namespace in self.namespaces:
            if not hasattr(conf, namespace):
                if not self._strict:
                    continue
                raise exc.NamespaceNotRegistered('The namespace {0} is not registered.'.format(namespace))
            name = getattr(conf, namespace)
            for item, value in compat.iteritems(self.items(namespace)):
                if not hasattr(name, item):
                    if not self._strict:
                        continue
                    raise exc.OptionNotRegistered('The option {0} is not registered.'.format(item))
                setattr(name, item, value)

        return conf

    @property
    def namespaces(self):
        """Get an iterable of str representing namespaces within the config."""
        raise NotImplementedError()

    def items(self, namespace):
        """Get a dictionary of entries under a given namespace."""
        raise NotImplementedError()

    def _read(self):
        """Open the file and return its contents."""
        with open(self.path, 'r') as (file_handle):
            content = file_handle.read()
        return compat.unicode(content)