# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/connection.py
# Compiled at: 2019-09-26 00:19:20
# Size of source mod 2**32: 3520 bytes
__doc__ = 'Network layer for MRP.'
import asyncio, logging
from pyatv.log import log_binary
from pyatv.mrp import chacha20
from pyatv.mrp import protobuf
from pyatv.mrp.variant import read_variant, write_variant
_LOGGER = logging.getLogger(__name__)

class MrpConnection(asyncio.Protocol):
    """MrpConnection"""

    def __init__(self, host, port, loop):
        """Initialize a new MrpConnection."""
        self.host = str(host)
        self.port = port
        self.loop = loop
        self.listener = None
        self._buffer = ''
        self._chacha = None
        self._transport = None

    def connection_made(self, transport):
        """Device connection was made."""
        _LOGGER.debug('Connected to device')
        self._transport = transport

    def connection_lost(self, exc):
        """Device connection was dropped."""
        _LOGGER.debug('Disconnected from device: %s', exc)
        self._transport = None

    def enable_encryption(self, output_key, input_key):
        """Enable encryption with the specified keys."""
        self._chacha = chacha20.Chacha20Cipher(output_key, input_key)

    @property
    def connected(self):
        """If a connection is open or not."""
        return self._transport is not None

    def connect(self):
        """Connect to device."""
        return self.loop.create_connection(lambda : self, self.host, self.port)

    def close(self):
        """Close connection to device."""
        if self._transport:
            self._transport.close()
        self._transport = None
        self._chacha = None

    def send(self, message):
        """Send message to device."""
        serialized = message.SerializeToString()
        log_binary(_LOGGER, '>> Send', Data=serialized)
        if self._chacha:
            serialized = self._chacha.encrypt(serialized)
            log_binary(_LOGGER, '>> Send', Encrypted=serialized)
        data = write_variant(len(serialized)) + serialized
        self._transport.write(data)
        _LOGGER.debug('>> Send: Protobuf=%s', message)

    def data_received(self, data):
        """Message was received from device."""
        self._buffer += data
        log_binary(_LOGGER, '<< Receive', Data=data)
        while self._buffer:
            length, raw = read_variant(self._buffer)
            if len(raw) < length:
                _LOGGER.debug('Require %d bytes but only %d in buffer', length, len(raw))
                break
            data = raw[:length]
            self._buffer = raw[length:]
            try:
                self._handle_message(data)
            except Exception:
                _LOGGER.error('Failed to handle message')

    def _handle_message(self, data):
        if self._chacha:
            data = self._chacha.decrypt(data)
            log_binary(_LOGGER, '<< Receive', Decrypted=data)
        parsed = protobuf.ProtocolMessage()
        parsed.ParseFromString(data)
        _LOGGER.debug('<< Receive: Protobuf=%s', parsed)
        if self.listener:
            self.listener.message_received(parsed)