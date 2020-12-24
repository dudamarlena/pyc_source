# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/LoggingWebsocketHandler.py
# Compiled at: 2019-07-23 03:05:48
# Size of source mod 2**32: 1455 bytes
import logging
from queue import Queue
import threading, time, traceback, websocket

class WebsocketHandler(logging.Handler):

    def __init__(self, url):
        logging.Handler.__init__(self)
        self.queue = queue = Queue()
        self.client = Websocket(url, queue)
        self.client.start()

    def emit(self, record):
        msg = self.format(record)
        self.queue.put(msg)


class Websocket:

    def __init__(self, url, queue):
        self.conn = None
        self.queue = queue
        self.url = url
        self.thread = None

    def start(self):
        self.thread = thread = threading.Thread(target=(self.main))
        thread.setDaemon(True)
        thread.start()

    def main(self):
        self.reconnect()
        while True:
            try:
                self.loop()
            except Exception as ex:
                self.handleError(ex)

    def handleError(self, ex):
        if isinstance(ex, ConnectionError):
            self.reconnect()
            return
        raise ex

    def reconnect(self):
        if self.conn:
            self.conn.shutdown()
        while True:
            try:
                self.conn = websocket.create_connection(self.url)
                break
            except ConnectionError:
                traceback.print_exc()
                time.sleep(1)

    def loop(self):
        msg = self.queue.get()
        self.conn.send(msg)