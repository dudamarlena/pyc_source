# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/discord_simple/models/message.py
# Compiled at: 2016-09-16 16:12:55
""" Todo """
from .user import User

class Message:
    """ Todo """
    author = None
    content = None
    timestamp = None
    channel_id = None

    def __init__(self, data):
        """ Todo """
        self.author = User(data.get('author', {}))
        self.content = data.get('content', '')
        self.timestamp = data.get('timestamp', 0)
        self.channel_id = data.get('channel_id', None)
        return