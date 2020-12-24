# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditz/__init__.py
# Compiled at: 2016-03-07 14:40:46
"""
Python implementation of Ditz (http://rubygems.org/gems/ditz).
"""
import pkg_resources as pkg
from .plugin import loader
path = pkg.resource_filename(__name__, 'plugins')
loader.add_path(path)
del path
del loader
del pkg