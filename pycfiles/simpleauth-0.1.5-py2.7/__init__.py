# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/simpleauth/__init__.py
# Compiled at: 2014-10-02 11:25:18
"""
A simple auth handler for Google App Engine supporting
OAuth 1.0a, 2.0 and OpenID.
"""
__version__ = '0.1.5'
__license__ = 'MIT'
__author__ = 'Alex Vaghin (alex@cloudware.it)'
__all__ = []
from handler import *
__all__ += handler.__all__