# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/error.py
# Compiled at: 2008-01-19 12:32:25
"""Exception classes.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize

class Unauthorized(Exception):
    """The operation was not authorized."""
    pass


class ContextMismatch(Exception):
    """An object from a different restricted database was used."""
    pass


optimize.bind_all(sys.modules[__name__])