# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/colubrid/__init__.py
# Compiled at: 2006-09-10 14:22:28
__doc__ = '\n    Colubrid WSGI Toolkit\n    ---------------------\n'
__version__ = '0.10'
__author__ = 'Armin Ronacher <armin.ronacher@active-4.com>'
__license__ = 'BSD License'
from colubrid.application import *
from colubrid.request import Request
from colubrid.response import HttpResponse
from colubrid.server import execute