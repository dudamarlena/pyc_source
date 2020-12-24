# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/exceptions/loading.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 454 bytes
"""Exceptions related with imports of modules/attributes/scripts.
"""
from deephyper.core.exceptions import DeephyperError

class GenericLoaderError(DeephyperError):
    __doc__ = 'Raised when the generic_loader function is failing.\n    '

    def __init__(self, str_value):
        self.str_value = str_value

    def __str__(self):
        return f"The target '{self.str_value}' cannot be imported because it's neither a python script nor a python module."