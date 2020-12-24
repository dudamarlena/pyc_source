# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/package/cache.py
# Compiled at: 2019-01-22 13:34:55
# Size of source mod 2**32: 703 bytes
from collections import defaultdict
from typeguard import check_argument_types
from .loader import load

class PluginCache(defaultdict):
    __doc__ = 'Lazily load plugins from the given namespace.\n\t\n\tSupports read-only dictionary-like and attribute access.\n\t'

    def __init__(self, namespace):
        """You must specify an entry point namespace."""
        assert check_argument_types()
        super().__init__()
        self.namespace = namespace

    def __missing__(self, key):
        """If not already loaded, attempt to load the reference."""
        self[key] = load(key, self.namespace)
        return self[key]

    def __getattr__(self, name):
        """Proxy attribute access through to the dictionary."""
        return self[name]