# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/monolith/build/lib/monolith/compat.py
# Compiled at: 2013-11-30 15:42:16
# Size of source mod 2**32: 607 bytes
"""
This module provides utilities or wraps existing modules/packages into
tools universal across supported Python versions.
"""
import sys
try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from collections import OrderedDict
except ImportError:
    from monolith.utils.ordereddict import OrderedDict

try:
    str = str
except NameError:
    str = str = str

if sys.version_info < (2, 7):
    from contextlib import nested
else:

    def nested(*context_managers):
        return tuple(context_managers)


__all__ = [
 'unittest', 'OrderedDict', 'nested', 'unicode']