# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/admin/import_utils.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals

def has_module(module_name, members=[]):
    """Return whether or not a given module can be imported."""
    try:
        mod = __import__(module_name, fromlist=members)
    except ImportError:
        return False

    for member in members:
        if not hasattr(mod, member):
            return False

    return True