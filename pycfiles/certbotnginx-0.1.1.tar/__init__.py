# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/certbotlib/__init__.py
# Compiled at: 2017-10-06 09:11:33
__doc__ = '\ncertbotlib package\n\nImports all parts from certbotlib here\n'
from ._version import __version__
from .certbotlib import Certbot
__author__ = 'Oriol Fabregas'
__email__ = 'oriol.fabregas@payconiq.com'
assert __version__
assert Certbot