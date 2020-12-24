# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/core/middleware.py
# Compiled at: 2013-08-08 04:50:11
from django.contrib.auth.middleware import RemoteUserMiddleware

class CustomHeaderMiddleware(RemoteUserMiddleware):
    """
    Authentication is done by httpd server and certificate DN is passed as a username to web application.
    """
    header = 'SSL_CLIENT_S_DN'