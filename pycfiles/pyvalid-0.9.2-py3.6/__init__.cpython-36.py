# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pyvalid/__init__.py
# Compiled at: 2018-06-02 18:06:28
# Size of source mod 2**32: 424 bytes
from pyvalid.__accepts import Accepts
from pyvalid.__returns import Returns
from pyvalid.__exceptions import InvalidArgumentNumberError, InvalidReturnType, ArgumentValidationError
accepts = Accepts
returns = Returns
version = '0.9.2'
__all__ = [
 'validators',
 'switch',
 'version',
 'accepts',
 'returns',
 'InvalidArgumentNumberError',
 'InvalidReturnType',
 'ArgumentValidationError']