# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/__init__.py
# Compiled at: 2018-07-08 23:37:16
# Size of source mod 2**32: 382 bytes
"""maxiPago python integration"""
VERSION = (1, 1, 1)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__author__ = 'Stored'
__contact__ = 'contato@stored.com.br'
__docformat__ = 'restructuredtext'
__license__ = 'MIT'
from maxipago.client import Maxipago