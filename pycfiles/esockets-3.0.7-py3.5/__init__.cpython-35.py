# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ESocketS/__init__.py
# Compiled at: 2015-12-25 07:52:53
# Size of source mod 2**32: 172 bytes
from ESocketS.socket_server import Socket
from ESocketS.exceptions import *
with open(__path__[0] + '/version', 'r') as (r):
    __version__ = r.read()