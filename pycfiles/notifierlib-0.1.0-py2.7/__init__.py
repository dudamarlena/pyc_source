# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifierlib/__init__.py
# Compiled at: 2017-09-18 11:05:17
"""
notifierlib package

Imports all parts from notifierlib here
"""
from ._version import __version__
from notifierlib import Notifier, Group
from channels.email import Email
from channels.stdout import Stdout
__author__ = 'Costas Tyfoxylos'
__email__ = 'costas.tyf@gmail.com'
__version__ = __version__
assert __version__
assert Notifier
assert Group
assert Email
assert Stdout