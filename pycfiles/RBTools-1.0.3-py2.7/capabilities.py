# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/api/capabilities.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals

class Capabilities(object):
    """Stores and retrieves Review Board server capabilities."""

    def __init__(self, capabilities):
        self.capabilities = capabilities

    def has_capability(self, *args):
        caps = self.capabilities
        try:
            for arg in args:
                caps = caps[arg]

            return caps is True
        except (TypeError, KeyError):
            return False