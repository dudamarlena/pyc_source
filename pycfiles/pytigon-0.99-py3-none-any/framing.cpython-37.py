# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/websockets/websockets/framing.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 10244 bytes
"""
:mod:`websockets.framing` reads and writes WebSocket frames.

It deals with a single frame at a time. Anything that depends on the sequence
of frames is implemented in :mod:`websockets.protocol`.

See `section 5 of RFC 6455`_.

.. _section 5 of RFC 6455: http://tools.ietf.org/html/rfc6455#section-5

"""
import io, random, struct
from typing import Any, Awaitable, Callable, NamedTuple, Optional, Sequence, Tuple
from .exceptions import PayloadTooBig, ProtocolError
from .typing import Data
try:
    from .speedups import apply_mask
except ImportError:
    from .utils import apply_mask

__all__ = [
 'DATA_OPCODES',
 'CTRL_OPCODES',
 'OP_CONT',
 'OP_TEXT',
 'OP_BINARY',
 'OP_CLOSE',
 'OP_PING',
 'OP_PONG',
 'Frame',
 'prepare_data',
 'encode_data',
 'parse_close',
 'serialize_close']
DATA_OPCODES = OP_CONT, OP_TEXT, OP_BINARY = (0, 1, 2)
CTRL_OPCODES = OP_CLOSE, OP_PING, OP_PONG = (8, 9, 10)
EXTERNAL_CLOSE_CODES = [
 1000, 1001, 1002, 1003, 1007, 1008, 1009, 1010, 1011]

class Frame(NamedTuple):
    __doc__ = '\n    WebSocket frame.\n\n    :param bool fin: FIN bit\n    :param bool rsv1: RSV1 bit\n    :param bool rsv2: RSV2 bit\n    :param bool rsv3: RSV3 bit\n    :param int opcode: opcode\n    :param bytes data: payload data\n\n    Only these fields are needed. The MASK bit, payload length and masking-key\n    are handled on the fly by :meth:`read` and :meth:`write`.\n\n    '
    fin: bool
    opcode: int
    data: bytes
    rsv1 = False
    rsv1: bool
    rsv2 = False
    rsv2: bool
    rsv3 = False
    rsv3: bool

    @classmethod
    async def read(cls, reader: Callable[([int], Awaitable[bytes])], *, mask: bool, max_size: Optional[int]=None, extensions: Optional[Sequence['websockets.extensions.base.Extension']]=None) -> 'Frame':
        """
        Read a WebSocket frame.

        :param reader: coroutine that reads exactly the requested number of
            bytes, unless the end of file is reached
        :param mask: whether the frame should be masked i.e. whether the read
            happens on the server side
        :param max_size: maximum payload size in bytes
        :param extensions: list of classes with a ``decode()`` method that
            transforms the frame and return a new frame; extensions are applied
            in reverse order
        :raises ~websockets.exceptions.PayloadTooBig: if the frame exceeds
            ``max_size``
        :raises ~websockets.exceptions.ProtocolError: if the frame
            contains incorrect values

        """
        data = await reader(2)
        head1, head2 = struct.unpack('!BB', data)
        fin = True if head1 & 128 else False
        rsv1 = True if head1 & 64 else False
        rsv2 = True if head1 & 32 else False
        rsv3 = True if head1 & 16 else False
        opcode = head1 & 15
        if (True if head2 & 128 else False) != mask:
            raise ProtocolError('incorrect masking')
        length = head2 & 127
        if length == 126:
            data = await reader(2)
            length, = struct.unpack('!H', data)
        else:
            if length == 127:
                data = await reader(8)
                length, = struct.unpack('!Q', data)
            elif max_size is not None and length > max_size:
                raise PayloadTooBig(f"payload length exceeds size limit ({length} > {max_size} bytes)")
            if mask:
                mask_bits = await reader(4)
            data = await reader(length)
            if mask:
                data = apply_mask(data, mask_bits)
            frame = cls(fin, opcode, data, rsv1, rsv2, rsv3)
            if extensions is None:
                extensions = []
            for extension in reversed(extensions):
                frame = extension.decode(frame, max_size=max_size)

            frame.check()
            return frame

    def write(frame, write: Callable[([bytes], Any)], *, mask: bool, extensions: Optional[Sequence['websockets.extensions.base.Extension']]=None) -> None:
        """
        Write a WebSocket frame.

        :param frame: frame to write
        :param write: function that writes bytes
        :param mask: whether the frame should be masked i.e. whether the write
            happens on the client side
        :param extensions: list of classes with an ``encode()`` method that
            transform the frame and return a new frame; extensions are applied
            in order
        :raises ~websockets.exceptions.ProtocolError: if the frame
            contains incorrect values

        """
        frame.check()
        if extensions is None:
            extensions = []
        else:
            for extension in extensions:
                frame = extension.encode(frame)

            output = io.BytesIO()
            head1 = (128 if frame.fin else 0) | (64 if frame.rsv1 else 0) | (32 if frame.rsv2 else 0) | (16 if frame.rsv3 else 0) | frame.opcode
            head2 = 128 if mask else 0
            length = len(frame.data)
            if length < 126:
                output.write(struct.pack('!BB', head1, head2 | length))
            else:
                if length < 65536:
                    output.write(struct.pack('!BBH', head1, head2 | 126, length))
                else:
                    output.write(struct.pack('!BBQ', head1, head2 | 127, length))
            if mask:
                mask_bits = struct.pack('!I', random.getrandbits(32))
                output.write(mask_bits)
            if mask:
                data = apply_mask(frame.data, mask_bits)
            else:
                data = frame.data
        output.write(data)
        write(output.getvalue())

    def check(frame) -> None:
        """
        Check that reserved bits and opcode have acceptable values.

        :raises ~websockets.exceptions.ProtocolError: if a reserved
            bit or the opcode is invalid

        """
        if not frame.rsv1:
            if frame.rsv2 or frame.rsv3:
                raise ProtocolError('reserved bits must be 0')
            if frame.opcode in DATA_OPCODES:
                return
            if frame.opcode in CTRL_OPCODES:
                if len(frame.data) > 125:
                    raise ProtocolError('control frame too long')
                if not frame.fin:
                    raise ProtocolError('fragmented control frame')
        else:
            raise ProtocolError(f"invalid opcode: {frame.opcode}")


def prepare_data(data: Data) -> Tuple[(int, bytes)]:
    """
    Convert a string or byte-like object to an opcode and a bytes-like object.

    This function is designed for data frames.

    If ``data`` is a :class:`str`, return ``OP_TEXT`` and a :class:`bytes`
    object encoding ``data`` in UTF-8.

    If ``data`` is a bytes-like object, return ``OP_BINARY`` and a bytes-like
    object.

    :raises TypeError: if ``data`` doesn't have a supported type

    """
    if isinstance(data, str):
        return (
         OP_TEXT, data.encode('utf-8'))
        if isinstance(data, (bytes, bytearray)):
            return (
             OP_BINARY, data)
        if isinstance(data, memoryview):
            if data.c_contiguous:
                return (
                 OP_BINARY, data)
            return (OP_BINARY, data.tobytes())
    else:
        raise TypeError('data must be bytes-like or str')


def encode_data(data: Data) -> bytes:
    """
    Convert a string or byte-like object to bytes.

    This function is designed for ping and pong frames.

    If ``data`` is a :class:`str`, return a :class:`bytes` object encoding
    ``data`` in UTF-8.

    If ``data`` is a bytes-like object, return a :class:`bytes` object.

    :raises TypeError: if ``data`` doesn't have a supported type

    """
    if isinstance(data, str):
        return data.encode('utf-8')
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    raise TypeError('data must be bytes-like or str')


def parse_close(data: bytes) -> Tuple[(int, str)]:
    """
    Parse the payload from a close frame.

    Return ``(code, reason)``.

    :raises ~websockets.exceptions.ProtocolError: if data is ill-formed
    :raises UnicodeDecodeError: if the reason isn't valid UTF-8

    """
    length = len(data)
    if length >= 2:
        code, = struct.unpack('!H', data[:2])
        check_close(code)
        reason = data[2:].decode('utf-8')
        return (code, reason)
    if length == 0:
        return (1005, '')
    assert length == 1
    raise ProtocolError('close frame too short')


def serialize_close(code: int, reason: str) -> bytes:
    """
    Serialize the payload for a close frame.

    This is the reverse of :func:`parse_close`.

    """
    check_close(code)
    return struct.pack('!H', code) + reason.encode('utf-8')


def check_close(code: int) -> None:
    """
    Check that the close code has an acceptable value for a close frame.

    :raises ~websockets.exceptions.ProtocolError: if the close code
        is invalid

    """
    if not code in EXTERNAL_CLOSE_CODES:
        if not 3000 <= code < 5000:
            raise ProtocolError('invalid status code')


import websockets.extensions.base