# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/certbotlib/__init__.py
# Compiled at: 2017-10-06 09:11:33
"""
certbotlib package

Imports all parts from certbotlib here
"""
from ._version import __version__
from .certbotlib import Certbot
__author__ = 'Oriol Fabregas'
__email__ = 'oriol.fabregas@payconiq.com'
assert __version__
assert Certbot