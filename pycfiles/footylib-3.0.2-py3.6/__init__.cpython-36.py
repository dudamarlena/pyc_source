# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/footylib/__init__.py
# Compiled at: 2018-01-20 06:33:15
# Size of source mod 2**32: 215 bytes
from ._version import __version__
from .footylib import Footy, FootyEvent
from .footylibExceptions import *
__author__ = 'Oriol Fabregas'
if not __version__:
    raise AssertionError
else:
    assert Footy
    assert FootyEvent