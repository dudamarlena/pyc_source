# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.4.1-x86_64/egg/esix/__init__.py
# Compiled at: 2016-08-24 18:59:30
"""
High level frontend for the e621 JSON API.
"""
__version__ = '1.3.1'
__author__ = 'Alex Schaeffer'
__copyright__ = 'Copyright (c)2014, ' + __author__
__all__ = [
 'api', 'config', 'errors', 'post', 'comment', 'user',
 'tag', 'pool', 'takedown', 'forum', 'ticket']
from . import *