# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/connectrum/protocol.py
# Compiled at: 2020-03-27 11:48:43
# Size of source mod 2**32: 1963 bytes
import asyncio, json, logging
logger = logging.getLogger(__name__)

class StratumProtocol(asyncio.Protocol):
    client = None
    closed = False
    transport = None
    buf = b''

    def connection_made(self, transport):
        self.transport = transport
        logger.debug('Transport connected ok')

    def connection_lost(self, exc):
        if not self.closed:
            self.closed = True
            self.close()
            self.client._connection_lost(self)

    def data_received(self, data):
        self.buf += data
        *lines, self.buf = self.buf.split(b'\n')
        for line in lines:
            if not line:
                continue
            try:
                msg = line.decode('utf-8', 'error').strip()
            except UnicodeError as exc:
                try:
                    logger.exception('Encoding issue on %r' % line)
                    self.connection_lost(exc)
                    return
                finally:
                    exc = None
                    del exc

            try:
                msg = json.loads(msg)
            except ValueError as exc:
                try:
                    logger.exception('Bad JSON received from server: %r' % msg)
                    self.connection_lost(exc)
                    return
                finally:
                    exc = None
                    del exc

            try:
                self.client._got_response(msg)
            except Exception as e:
                try:
                    logger.exception('Trouble handling response! (%s)' % e)
                    continue
                finally:
                    e = None
                    del e

    def send_data(self, message):
        """
            Given an object, encode as JSON and transmit to the server.
        """
        data = json.dumps(message).encode('utf-8') + b'\n'
        self.transport.write(data)

    def close(self):
        if not self.closed:
            try:
                self.transport.close()
            finally:
                self.closed = True