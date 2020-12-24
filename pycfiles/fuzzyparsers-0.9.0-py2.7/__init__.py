# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fuzzyparsers/__init__.py
# Compiled at: 2014-02-05 08:01:00
"""
fuzzyparsers library initialization
"""
from .strings import default_match, fuzzy_match
from .dates import *
__version_info__ = [
 '0', '9', '0']
__version__ = ('.').join(__version_info__)