# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_internal/models/format_control.py
# Compiled at: 2019-02-14 00:35:06
from pip._vendor.packaging.utils import canonicalize_name
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, Set, FrozenSet

class FormatControl(object):
    """Helper for managing formats from which a package can be installed.
    """

    def __init__(self, no_binary=None, only_binary=None):
        if no_binary is None:
            no_binary = set()
        if only_binary is None:
            only_binary = set()
        self.no_binary = no_binary
        self.only_binary = only_binary
        return

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return ('{}({}, {})').format(self.__class__.__name__, self.no_binary, self.only_binary)

    @staticmethod
    def handle_mutual_excludes(value, target, other):
        new = value.split(',')
        while ':all:' in new:
            other.clear()
            target.clear()
            target.add(':all:')
            del new[:new.index(':all:') + 1]
            if ':none:' not in new:
                return

        for name in new:
            if name == ':none:':
                target.clear()
                continue
            name = canonicalize_name(name)
            other.discard(name)
            target.add(name)

    def get_allowed_formats(self, canonical_name):
        result = {
         'binary', 'source'}
        if canonical_name in self.only_binary:
            result.discard('source')
        elif canonical_name in self.no_binary:
            result.discard('binary')
        elif ':all:' in self.only_binary:
            result.discard('source')
        elif ':all:' in self.no_binary:
            result.discard('binary')
        return frozenset(result)

    def disallow_binaries(self):
        self.handle_mutual_excludes(':all:', self.no_binary, self.only_binary)