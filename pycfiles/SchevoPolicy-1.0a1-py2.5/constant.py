# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/constant.py
# Compiled at: 2008-01-19 12:32:25
"""Constants.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo.constant import _GLOBAL, _FALSE

class ALLOW(object):
    """Allow an operation."""
    __metaclass__ = _GLOBAL


class DENY(object):
    """Deny an operation."""
    __metaclass__ = _FALSE


optimize.bind_all(sys.modules[__name__])