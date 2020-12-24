# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/validino/__init__.py
# Compiled at: 2007-12-06 13:09:46
"""
A data conversion and validation package.

In typical use, you create a Schema with
various subvalidators.  For instance:
>>> import validino as V
>>> validators=dict(username=(V.strip,
...                           V.not_empty('Pledge enter a username'),
...                           V.clamp_length(max=20)),
...                 password=V.not_empty('Please enter a password'))
>>> s=V.Schema(validators)
>>> confirmed=s(dict(username='henry', password='dogwood'))
"""
from validino.base import *
from validino.extra import *
from validino.messages import *
from validino.field import *
__version__ = '0.2.2'