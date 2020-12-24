# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cuiows/wsproto/frame_protocol.py
# Compiled at: 2017-01-22 09:55:14
# Size of source mod 2**32: 15563 bytes
"""
wsproto/frame_protocol
~~~~~~~~~~~~~~

WebSocket frame protocol implementation.
"""
import os, itertools, struct
from codecs import getincrementaldecoder
from collections import namedtuple
from enum import Enum, IntEnum
try:
    from wsaccel.xormask import XorMaskerSimple
except ImportError:

    class XorMaskerSimple:

        def __init__(self, masking_key):
            self._maskbytes = itertools.cycle(masking_key)

        def process(self, data):
            maskbytes = self._maskbytes
            return bytes(b ^ next(maskbytes) for b in data)


class XorMaskerNull:

    def process(self, data):
        return data


MAX_FRAME_PAYLOAD = 18446744073709551616

class Opcode(IntEnum):
    __doc__ = '\n    RFC 6455, Section 5.2 - Base Framing Protocol\n    '
    CONTINUATION = 0
    TEXT = 1
    BINARY = 2
    CLOSE = 8
    PING = 9
    PONG = 10

    def iscontrol(self):
        return bool(self & 8)


class CloseReason(IntEnum):
    __doc__ = '\n    RFC 6455, Section 7.4.1 - Defined Status Codes\n    '
    NORMAL_CLOSURE = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    UNSUPPORTED_DATA = 1003
    NO_STATUS_RCVD = 1005
    ABNORMAL_CLOSURE = 1006
    INVALID_FRAME_PAYLOAD_DATA = 1007
    POLICY_VIOLATION = 1008
    MESSAGE_TOO_BIG = 1009
    MANDATORY_EXT = 1010
    INTERNAL_ERROR = 1011
    SERVICE_RESTART = 1012
    TRY_AGAIN_LATER = 1013
    TLS_HANDSHAKE_FAILED = 1015


LOCAL_ONLY_CLOSE_REASONS = (
 CloseReason.NO_STATUS_RCVD,
 CloseReason.ABNORMAL_CLOSURE,
 CloseReason.TLS_HANDSHAKE_FAILED)
NULL_MASK = struct.pack('!I', 0)

class ParseFailed(Exception):

    def __init__(self, msg, code=CloseReason.PROTOCOL_ERROR):
        super().__init__(msg)
        self.code = code


Header = namedtuple('Header', 'fin rsv opcode payload_len masking_key'.split())
Frame = namedtuple('Frame', 'opcode payload frame_finished message_finished'.split())

def _truncate_utf8(data, nbytes):
    if len(data) <= nbytes:
        return data
    else:
        data = data[:nbytes]
        data = data.decode('utf-8', errors='ignore').encode('utf-8')
        return data


class FrameProtocol(object):

    class State(Enum):
        HEADER = 1
        PAYLOAD = 2
        FRAME_COMPLETE = 3
        FAILED = 4

    def __init__(self, client, extensions):
        self.client = client
        self.extensions = extensions
        self._buffer = bytearray()
        self._parse_more = self.parse_more_gen()
        self._outbound_opcode = None

    def _consume_at_most(self, nbytes):
        if not nbytes:
            return bytearray()
        while not self._buffer:
            yield

        data = self._buffer[:nbytes]
        del self._buffer[:nbytes]
        return data

    def _consume_exactly(self, nbytes):
        while len(self._buffer) < nbytes:
            yield

        return (yield from self._consume_at_most(nbytes))

    def _parse_header(self):
        fin_rsv_opcode, = yield from self._consume_exactly(1)
        fin = bool(fin_rsv_opcode & 128)
        rsv = (bool(fin_rsv_opcode & 64),
         bool(fin_rsv_opcode & 32),
         bool(fin_rsv_opcode & 16))
        opcode = fin_rsv_opcode & 15
        try:
            opcode = Opcode(opcode)
        except ValueError:
            raise ParseFailed('Invalid opcode {:#x}'.format(opcode))

        if opcode.iscontrol() and not fin:
            raise ParseFailed('Invalid attempt to fragment control frame')
        mask_len, = yield from self._consume_exactly(1)
        has_mask = bool(mask_len & 128)
        payload_len = mask_len & 127
        if opcode.iscontrol() and payload_len > 125:
            raise ParseFailed('Control frame with payload len > 125')
        if payload_len == 126:
            data = yield from self._consume_exactly(2)
            payload_len, = struct.unpack('!H', data)
            if payload_len <= 125:
                raise ParseFailed('Payload length used 2 bytes when 1 would have sufficed')
        else:
            if payload_len == 127:
                data = yield from self._consume_exactly(8)
                payload_len, = struct.unpack('!Q', data)
                if payload_len < 65536:
                    raise ParseFailed('Payload length used 8 bytes when 2 would have sufficed')
                if payload_len >> 63:
                    raise ParseFailed('8-byte payload length with non-zero MSB')
                for extension in self.extensions:
                    result = extension.frame_inbound_header(self, opcode, rsv, payload_len)
                    if result is not None:
                        raise ParseFailed('error in extension', result)

                if not self.extensions and True in rsv:
                    raise ParseFailed('Reserved bit set unexpectedly')
                if has_mask and self.client:
                    raise ParseFailed('client received unexpected masked frame')
                if not has_mask and not self.client:
                    raise ParseFailed('server received unexpected unmasked frame')
                if has_mask:
                    masking_key = yield from self._consume_exactly(4)
            else:
                masking_key = NULL_MASK
        return Header(fin, rsv, opcode, payload_len, masking_key)

    def _process_payload_chunk(self, masker, data):
        data = masker.process(data)
        for extension in self.extensions:
            data = extension.frame_inbound_payload_data(self, data)
            if isinstance(data, CloseReason):
                raise ParseFailed('error in extension', data)

        return data

    def _process_payload_complete(self, fin):
        final = bytearray()
        for extension in self.extensions:
            result = extension.frame_inbound_complete(self, fin)
            if isinstance(result, CloseReason):
                raise ParseFailed('error in extension', result)
            if result is not None:
                final += result

        return final

    def _process_CLOSE_payload(self, data):
        if len(data) == 0:
            return (
             CloseReason.NO_STATUS_RCVD, '')
        if len(data) == 1:
            raise ParseFailed('CLOSE with 1 byte payload')
        else:
            code, = struct.unpack('!H', data[:2])
            if code < 1000:
                raise ParseFailed('CLOSE with invalid code')
            try:
                code = CloseReason(code)
            except ValueError:
                pass

            if code in LOCAL_ONLY_CLOSE_REASONS:
                raise ParseFailed('remote CLOSE with local-only reason')
            if not isinstance(code, CloseReason) and code < 3000:
                raise ParseFailed('CLOSE with unknown reserved code')
            try:
                reason = data[2:].decode('utf-8')
            except UnicodeDecodeError as exc:
                raise ParseFailed('Error decoding CLOSE reason: ' + str(exc), CloseReason.INVALID_FRAME_PAYLOAD_DATA)

            return (
             code, reason)

    def parse_more_gen(self):
        self.extensions = [ext for ext in self.extensions if ext.enabled()]
        unfinished_message_opcode = None
        unfinished_message_decoder = None
        while 1:
            header = yield from self._parse_header()
            if unfinished_message_opcode is None:
                if header.opcode is Opcode.CONTINUATION:
                    raise ParseFailed('unexpected CONTINUATION')
                elif not header.opcode.iscontrol():
                    unfinished_message_opcode = header.opcode
            else:
                if not header.opcode.iscontrol() and header.opcode is not Opcode.CONTINUATION:
                    raise ParseFailed('expected CONTINUATION, not {!r}'.format(header.opcode))
                effective_opcode = header.opcode
                if effective_opcode is Opcode.CONTINUATION:
                    effective_opcode = unfinished_message_opcode
                if header.masking_key == NULL_MASK:
                    masker = XorMaskerNull()
                else:
                    masker = XorMaskerSimple(header.masking_key)
                if unfinished_message_opcode is Opcode.TEXT and unfinished_message_decoder is None:
                    unfinished_message_decoder = getincrementaldecoder('utf-8')()
            remaining = header.payload_len
            frame_finished = False
            while not frame_finished:
                if effective_opcode.iscontrol():
                    data = yield from self._consume_exactly(remaining)
                else:
                    data = yield from self._consume_at_most(remaining)
                remaining -= len(data)
                frame_finished = remaining == 0
                message_finished = frame_finished and header.fin
                data = self._process_payload_chunk(masker, data)
                if frame_finished:
                    data += self._process_payload_complete(header.fin)
                if effective_opcode is Opcode.CLOSE:
                    data = self._process_CLOSE_payload(data)
                if not effective_opcode.iscontrol():
                    if unfinished_message_decoder is not None:
                        try:
                            data = unfinished_message_decoder.decode(data, message_finished)
                        except UnicodeDecodeError as exc:
                            raise ParseFailed(str(exc), CloseReason.INVALID_FRAME_PAYLOAD_DATA)

                        if message_finished:
                            unfinished_message_opcode = None
                            unfinished_message_decoder = None
                        yield Frame(effective_opcode, data, frame_finished, message_finished)

            if effective_opcode is Opcode.CLOSE:
                break

    def receive_bytes(self, data):
        self._buffer += data

    def received_frames(self):
        for event in self._parse_more:
            if event is None:
                break
            else:
                yield event

    def close(self, code=None, reason=None):
        payload = bytearray()
        if code is None and reason is not None:
            raise TypeError('cannot specify a reason without a code')
        if code in LOCAL_ONLY_CLOSE_REASONS:
            code = CloseReason.NORMAL_CLOSURE
        if code is not None:
            payload += struct.pack('!H', code)
            if reason is not None:
                payload += _truncate_utf8(reason.encode('utf-8'), 123)
        return self._serialize_frame(Opcode.CLOSE, payload)

    def pong(self, payload=None):
        return self._serialize_frame(Opcode.PONG, payload)

    def send_data(self, payload=b'', fin=True):
        if isinstance(payload, (bytes, bytearray, memoryview)):
            opcode = Opcode.BINARY
        else:
            if isinstance(payload, str):
                opcode = Opcode.TEXT
                payload = payload.encode('utf-8')
            if self._outbound_opcode is None:
                self._outbound_opcode = opcode
            else:
                if self._outbound_opcode is not opcode:
                    raise TypeError('Data type mismatch inside message')
                else:
                    opcode = Opcode.CONTINUATION
            if fin:
                self._outbound_opcode = None
        return self._serialize_frame(opcode, payload, fin)

    def _serialize_frame(self, opcode, payload=b'', fin=True):
        rsv = (False, False, False)
        for extension in reversed(self.extensions):
            if not extension.enabled():
                pass
            else:
                rsv, payload = extension.frame_outbound(self, opcode, rsv, payload, fin)

        fin_rsv = 0
        for bit in rsv:
            fin_rsv <<= 1
            fin_rsv |= int(bit)

        fin_rsv |= int(fin) << 3
        fin_rsv_opcode = fin_rsv << 4 | opcode
        payload_length = len(payload)
        quad_payload = False
        if payload_length <= 125:
            first_payload = payload_length
            second_payload = None
        else:
            if payload_length <= 65535:
                first_payload = 126
                second_payload = payload_length
            else:
                first_payload = 127
                second_payload = payload_length
                quad_payload = True
        if self.client:
            first_payload |= 128
        header = bytes([fin_rsv_opcode, first_payload])
        if second_payload is not None:
            if opcode.iscontrol():
                raise ValueError('payload too long for control frame')
            if quad_payload:
                header += struct.pack('!Q', second_payload)
            else:
                header += struct.pack('!H', second_payload)
            if self.client:
                pass
            masking_key = os.urandom(4)
            masker = XorMaskerSimple(masking_key)
            return header + masking_key + masker.process(payload)
        else:
            return header + payload