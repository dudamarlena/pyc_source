# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/roles/viewers/webui/web.py
# Compiled at: 2015-04-04 17:41:52
from __future__ import absolute_import, unicode_literals
import logging
from tornado import gen
from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
logger = logging.getLogger(__name__)

class IndexHandler(RequestHandler):

    def get(self):
        self.render(b'index.html')


class LogWebSocket(WebSocketHandler):

    @gen.coroutine
    def open(self):
        logger.info(b'Client connected.')
        self.application.ws.append(self)

    def on_close(self):
        logger.debug(b'Connection closed.')
        self.application.ws.remove(self)