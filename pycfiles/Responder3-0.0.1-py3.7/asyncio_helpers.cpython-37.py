# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\victim\Desktop\Responder3\responder3\core\asyncio_helpers.py
# Compiled at: 2019-04-29 07:33:30
# Size of source mod 2**32: 3087 bytes
import asyncio

async def generic_read(reader, n):
    return reader.read(n)


async def generic_write(writer, data):
    writer.write(data)
    await writer.drain()


async def readexactly_or_exc(reader, n, timeout=None):
    """
        Helper function to read exactly N amount of data from the wire.
        :param reader: The reader object
        :type reader: asyncio.StreamReader
        :param n: The maximum amount of bytes to read.
        :type n: int
        :param timeout: Time in seconds to wait for the reader to return data
        :type timeout: int
        :return: bytearray
        """
    temp = await (asyncio.gather)(*[asyncio.wait_for((reader.readexactly(n)), timeout=timeout)], **{'return_exceptions': True})
    if isinstance(temp[0], bytes):
        return temp[0]
    raise temp[0]
    return data


async def read_or_exc(reader, n, timeout=None):
    """
        Helper function to read N amount of data from the wire.
        :param reader: The reader object
        :type reader: asyncio.StreamReader
        :param n: The maximum amount of bytes to read. BEWARE: this only sets an upper limit of the data to be read
        :type n: int
        :param timeout: Time in seconds to wait for the reader to return data
        :type timeout: int
        :return: bytearray
        """
    temp = await (asyncio.gather)(*[asyncio.wait_for((reader.read(n)), timeout=timeout)], **{'return_exceptions': True})
    if isinstance(temp[0], bytes):
        return temp[0]
    raise temp[0]
    return data


async def readuntil_or_exc(reader, pattern, timeout=None):
    """
        Helper function to read the wire until a certain pattern is reached.
        :param reader: The reader object
        :type reader: asyncio.StreamReader
        :param pattern: The pattern marking the end of read
        :type pattern: bytearray
        :param timeout: Time in seconds to wait for the reader to reach the pattern
        :type timeout: int
        :return: bytearray
        """
    temp = await (asyncio.gather)(*[asyncio.wait_for((reader.readuntil(pattern)), timeout=timeout)], **{'return_exceptions': True})
    if isinstance(temp[0], bytes):
        return temp[0]
    raise temp[0]


async def readline_or_exc(reader, timeout=None):
    """
        Helper function to read the wire until an end-of-line character is reached.
        :param reader: The reader object
        :type reader: asyncio.StreamReader
        :param timeout: Time in seconds to wait for the reader to reach the pattern
        :type timeout: int
        :return: bytearray
        """
    temp = await (asyncio.gather)(*[asyncio.wait_for((reader.readline()), timeout=timeout)], **{'return_exceptions': True})
    if isinstance(temp[0], bytes):
        return temp[0]
    raise temp[0]


async def sendall(writer, data):
    """
        Helper function that writes all the data to the wire
        :param writer: Writer object
        :type writer: asyncio.StreamWriter
        :param data: Data to be written
        :type data: bytearray
        :return: None
        """
    try:
        writer.write(data)
        await writer.drain()
    except Exception as e:
        try:
            raise R3ConnectionClosed()
        finally:
            e = None
            del e


class R3ConnectionClosed(Exception):
    pass


@asyncio.coroutine
async def wait_mp_event(event, aio_event):
    event.wait(timeout=None)
    aio_event.set()