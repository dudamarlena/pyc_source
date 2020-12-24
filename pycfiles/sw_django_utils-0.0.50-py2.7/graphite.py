# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djutils/graphite.py
# Compiled at: 2016-05-23 03:12:51
import time, socket
from django.conf import settings

def push(metric, value, timestamp=None, server=None, port=None):
    if not timestamp:
        timestamp = int(time.time())
    if not server:
        server = settings.GRAPHITE_HOST
    if not port:
        port = settings.GRAPHITE_PORT
    sock = socket.socket()
    sock.connect((server, int(port)))
    message = '%s %s %d\n' % (metric, value, timestamp)
    sock.sendall(message)
    sock.close()