# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/utils/extension.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from reviewboard.extensions.base import get_extension_manager

def get_powerpack_extension():
    """Return the current enabled instance of the Power Pack extension.

    This will look up and return the current instance for the process, if
    enabled.

    Returns:
        rbpowerpack.extension.PowerPackExtension:
        The extension instance, if enabled, or ``None`` otherwise.
    """
    return get_extension_manager().get_enabled_extension(b'rbpowerpack.extension.PowerPackExtension')