# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/__init__.py
# Compiled at: 2018-12-07 08:05:31
# Size of source mod 2**32: 732 bytes
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
from core.env import env, context, __PATH__ as path, register
from core.lib.crypto.crypto import key
from core.lib.logs import log
import core.lib.data.data as data
import core.lib.db.db as db
import core.request as request
from core.resource import resource, client, bind
import core.user as user
import core.app.app as app
import core.network.network as network
import core.node.node as node
from .core import handlers
context.init()