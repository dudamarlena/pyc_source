# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.3.0-Power_Macintosh/egg/simple_json/__init__.py
# Compiled at: 2005-12-31 18:15:03
"""
simple_json was renamed to simplejson to comply with PEP 8 module naming
conventions.  This is a compatibility shim.

%s/simple_json/simplejson/g
"""
__version__ = '1.1'
import warnings
warnings.warn('simple_json is deprecated due to rename, import simplejson instead', DeprecationWarning)
import pkg_resources
pkg_resources.require('simplejson')
import simplejson
from simplejson import *
__all__ = simplejson.__all__