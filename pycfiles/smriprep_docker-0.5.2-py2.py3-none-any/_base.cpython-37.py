# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/html5lib/_trie/_base.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 1013 bytes
from __future__ import absolute_import, division, unicode_literals
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

class Trie(Mapping):
    __doc__ = 'Abstract base class for tries'

    def keys(self, prefix=None):
        keys = super(Trie, self).keys()
        if prefix is None:
            return set(keys)
        return {x for x in keys if x.startswith(prefix)}

    def has_keys_with_prefix(self, prefix):
        for key in self.keys():
            if key.startswith(prefix):
                return True

        return False

    def longest_prefix(self, prefix):
        if prefix in self:
            return prefix
        for i in range(1, len(prefix) + 1):
            if prefix[:-i] in self:
                return prefix[:-i]

        raise KeyError(prefix)

    def longest_prefix_item(self, prefix):
        lprefix = self.longest_prefix(prefix)
        return (lprefix, self[lprefix])