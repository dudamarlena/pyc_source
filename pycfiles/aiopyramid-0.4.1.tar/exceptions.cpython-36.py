# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/exceptions.py
# Compiled at: 2014-09-26 18:30:48
# Size of source mod 2**32: 74 bytes
import greenlet

class WebsocketClosed(greenlet.GreenletExit):
    pass