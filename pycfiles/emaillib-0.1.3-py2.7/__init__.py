# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emaillib/__init__.py
# Compiled at: 2017-09-18 10:05:45
"""
emaillib package

Imports all parts from emaillib here
"""
from ._version import __version__
from .emaillib import SmtpServer, EasySender, Message
__author__ = 'Costas Tyfoxylos'
__email__ = 'costas.tyf@gmail.com'
assert __version__
assert __author__
assert __email__
assert SmtpServer
assert EasySender
assert Message