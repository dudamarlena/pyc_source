# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\IBGelf\handler.py
# Compiled at: 2011-10-26 06:26:58
import logging
try:
    import json
except ImportError:
    import simplejson as json

import zlib, traceback, struct, random, socket
from logging.handlers import DatagramHandler
(WAN_CHUNK, LAN_CHUNK) = (1420, 8154)

class GELFHandler(DatagramHandler):
    __module__ = __name__

    def __init__(self, host, port, chunk_size=WAN_CHUNK):
        self.chunk_size = chunk_size
        DatagramHandler.__init__(self, host, port)
        self.additionalFields = dict()

    def addAditionalField(self, key, value):
        self.additionalFields['_' + key] = value

    def send(self, s):
        if len(s) < self.chunk_size:
            DatagramHandler.send(self, s)
        else:
            for chunk in ChunkedGELF(s, self.chunk_size):
                DatagramHandler.send(self, chunk)

    def makePickle(self, record):
        message_dict = self.make_message_dict(record)
        return zlib.compress(json.dumps(message_dict))

    def convert_level_to_syslog(self, level):
        return {logging.CRITICAL: 2, logging.ERROR: 3, logging.WARNING: 4, logging.INFO: 6, logging.DEBUG: 7}.get(level, level)

    def get_full_message(self, exc_info):
        result = ''
        if exc_info:
            result = traceback.format_exc(exc_info)
        return result

    def make_message_dict(self, record):
        d = {'version': '1.0', 'host': socket.gethostname(), 'short_message': record.getMessage(), 'full_message': self.get_full_message(record.exc_info), 'timestamp': record.created, 'level': self.convert_level_to_syslog(record.levelno), 'facility': record.name, 'file': record.pathname, 'line': record.lineno}
        if hasattr(record, 'processName'):
            d['_process_name'] = record.processName
        for field in self.additionalFields.keys():
            d[field] = self.additionalFields[field]

        return d


class ChunkedGELF(object):
    __module__ = __name__

    def __init__(self, message, size):
        self.message = message
        self.size = size
        self.pieces = struct.pack('>H', len(message) / size + 1)
        self.id = struct.pack('Q', random.randint(0, 18446744073709551615)) * 4

    def message_chunks(self):
        return (self.message[i:i + self.size] for i in range(0, len(self.message), self.size))

    def encode(self, sequence, chunk):
        return ('').join(['\x1e\x0f', self.id, struct.pack('>H', sequence), self.pieces, chunk])

    def __iter__(self):
        for (sequence, chunk) in enumerate(self.message_chunks()):
            yield self.encode(sequence, chunk)