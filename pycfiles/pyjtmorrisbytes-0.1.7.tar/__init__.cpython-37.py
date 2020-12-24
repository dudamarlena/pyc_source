# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\jthec\Documents\github\jtmorrisbytes_flask_lib\src\pyjtmorrisbytes\__init__.py
# Compiled at: 2019-02-09 13:24:01
# Size of source mod 2**32: 590 bytes
""" The core package for all my flask apps
    ..moduleauthor:: Jordan Morris
    keywords: flask
    author: Jordan Taylor Morris
"""
__version__ = '0.1.3'
__liscense__ = 'MIT'
__title__ = 'pyjtmorrisbytes'
__srcurl__ = 'https://www.github.com/pyjtmorrisbytes/'
__url__ = 'https://www.jtmorrisbytes.com/'
__author__ = 'Jordan Taylor Morris jthecybertinkerer@gmail.com'
from . import factories
from . import models
from . import views
from . import controllers
from . import config