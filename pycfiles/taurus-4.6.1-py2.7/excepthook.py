# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/excepthook.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains a base class for exception hooks"""
import sys
from builtins import object
__all__ = [
 'BaseExceptHook']
__docformat__ = 'restructuredtext'

class BaseExceptHook(object):
    """A callable class that acts as an excepthook that handles an exception.
    This base class simply calls the :obj:`sys.__excepthook__`

    :param hook_to: callable excepthook that will be called at the end of
                    this hook handling [default: None]
    :type hook_to: callable"""

    def __init__(self, hook_to=None):
        self._excepthook = hook_to

    def __call__(self, *exc_info):
        self.report(*exc_info)
        if self._excepthook is not None:
            return self._excepthook(*exc_info)
        else:
            return

    def report(self, *exc_info):
        """Report an exception. Overwrite as necessary"""
        return sys.__excepthook__(*exc_info)