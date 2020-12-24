# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/io/tcpfns.py
# Compiled at: 2013-01-04 05:13:40
"""Subsidiary routines used to "pack" and "unpack" TCP messages. """
TCP_MAX_PACKET = 8192
LOG_MAX_MSG = 4

def pack_msg(msg):
    fmt = '%%0%dd' % LOG_MAX_MSG
    return fmt % len(msg) + msg


def unpack_msg(buf):
    length = int(buf[0:LOG_MAX_MSG])
    data = buf[LOG_MAX_MSG:LOG_MAX_MSG + length]
    buf = buf[LOG_MAX_MSG + length:]
    return (buf, data)


if __name__ == '__main__':
    msg = 'Hi there!'
    assert unpack_msg(pack_msg(msg))[1] == msg