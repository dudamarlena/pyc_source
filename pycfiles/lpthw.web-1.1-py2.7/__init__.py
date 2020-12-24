# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/web/__init__.py
# Compiled at: 2011-06-21 16:54:55
"""web.py: makes web apps (http://webpy.org)"""
from __future__ import generators
__version__ = '0.35'
__author__ = [
 'Aaron Swartz <me@aaronsw.com>',
 'Anand Chitipothu <anandology@gmail.com>']
__license__ = 'public domain'
__contributors__ = 'see http://webpy.org/changes'
import utils, db, net, wsgi, http, webapi, httpserver, debugerror, template, form, session
from utils import *
from db import *
from net import *
from wsgi import *
from http import *
from webapi import *
from httpserver import *
from debugerror import *
from application import *
from browser import *
try:
    import webopenid as openid
except ImportError:
    pass