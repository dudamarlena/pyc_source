# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/tcpfns.py
# Compiled at: 2017-08-03 17:13:00
"""Subsidiary routines used to "pack" and "unpack" TCP messages. """
TCP_MAX_PACKET = 8192
LOG_MAX_MSG = 4

def pack_msg(msg):
    fmt = '%%0%dd' % LOG_MAX_MSG
    return bytes(fmt % len(msg) + msg, 'UTF-8')


def unpack_msg(buf):
    if len(buf) == 0:
        return (
         '', bytes('q'.encode('utf-8')))
    length = int(buf[0:LOG_MAX_MSG])
    data = buf[LOG_MAX_MSG:LOG_MAX_MSG + length]
    buf = buf[LOG_MAX_MSG + length:]
    return (buf, data)


if __name__ == '__main__':
    print(unpack_msg(pack_msg('Hello, there!'))[1])