# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/pynexus/jsocket.py
# Compiled at: 2019-05-22 10:42:38
# Size of source mod 2**32: 3058 bytes
import json
from multiprocessing import Pipe
import uuid, websocket

class JSocketDecoder:

    def __init__(self, connection, chunk_size=2048):
        self.buf = ''
        self.decoder = json.JSONDecoder()
        self.connection = connection
        self.chunk_size = chunk_size
        self.obj_index = Pipe(False)
        self.objects = {}

    def storeObject(self, obj):
        uid = uuid.uuid4()
        self.objects[uid] = obj
        self.obj_index[1].send(uid)

    def getStoredObject(self):
        res = None
        if self.obj_index[0].poll():
            uid = self.obj_index[0].recv()
            res = self.objects[uid]
            del self.objects[uid]
        return res

    def recv(self):
        chunk = b''
        if type(self.connection) is websocket.WebSocket:
            chunk = self.connection.recv()
        else:
            incomplete = True
            while incomplete:
                chunk += self.connection.recv(self.chunk_size)
                try:
                    chunk = chunk.decode('utf8')
                    incomplete = False
                except:
                    pass

        return chunk

    def readObject(self):
        chunk = self.recv()
        if not chunk:
            raise Exception('Nexus Connection Closed')
        self.buf += chunk
        while self.buf:
            try:
                self.buf = self.buf.lstrip()
                res, index = self.decoder.raw_decode(self.buf)
                self.buf = self.buf[index:].lstrip()
                if res:
                    self.storeObject(res)
            except ValueError:
                self.buf += self.recv()

        return self.getStoredObject()

    def getObject(self):
        res = self.getStoredObject()
        if not res:
            res = self.readObject()
        return res

    def fileno(self):
        if self.obj_index[0].poll():
            return self.obj_index[0].fileno()
        return self.connection.fileno()