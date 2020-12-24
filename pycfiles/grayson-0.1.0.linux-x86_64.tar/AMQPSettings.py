# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/net/AMQPSettings.py
# Compiled at: 2012-05-03 13:20:58
import socket

class AMQPSettings(object):
    port
    hostname
    queue

    def __init__(port=5672, hostname=None, queue='default'):
        self.port = port
        self.hostname = hostname
        self.queue = queue