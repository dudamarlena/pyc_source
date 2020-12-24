# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sqlchemistry/exceptions.py
# Compiled at: 2008-04-15 10:14:47
"""Exceptions used with SQLChemistry

The base exception class is SQLChemistryError.

Copyright (C) 2008 Emanuel Gardaya Calso <egcalso@gmail.com>

This module is part of SQLChemistry and is is released under
the LGPL License
"""

class SQLChemistryError(Exception):
    """Generic error class."""
    pass


class SCDeprecationWarning(DeprecationWarning):
    """Issued once per usage of a deprecated API."""
    pass


class SCPendingDeprecationWarning(PendingDeprecationWarning):
    """Issued once per usage of a future deprecated API."""
    pass


class SCWarning(RuntimeWarning):
    """Issued at runtime."""
    pass