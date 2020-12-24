# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/exceptions.py
# Compiled at: 2014-09-26 18:30:48
# Size of source mod 2**32: 74 bytes
import greenlet

class WebsocketClosed(greenlet.GreenletExit):
    pass