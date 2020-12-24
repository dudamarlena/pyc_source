# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/user.py
# Compiled at: 2018-12-07 08:05:32
# Size of source mod 2**32: 245 bytes
from xio.core import peer

def user(*args, **kwargs):
    return (User.factory)(*args, **kwargs)


class User(peer.Peer):

    def __init__(self, **kwargs):
        (peer.Peer.__init__)(self, **kwargs)