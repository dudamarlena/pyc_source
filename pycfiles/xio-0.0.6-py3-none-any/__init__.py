# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/__init__.py
# Compiled at: 2018-12-07 08:05:31
"""
python2.7
 pip install bitcoin cffi

"""
try:
    from gevent import monkey
    monkey.patch_all()
except:
    pass

__version__ = '0.0.4'
from .core.env import env, context, __PATH__ as path, register
from .core.lib.crypto.crypto import key
from .core.lib.logs import log
from .core.lib.data.data import data
from .core.lib.db.db import db
from .core.request import request
from .core.resource import resource, client, bind
from .core.user import user
from .core.app.app import app
from .core.network.network import network
from .core.node.node import node
from .core import handlers
context.init()