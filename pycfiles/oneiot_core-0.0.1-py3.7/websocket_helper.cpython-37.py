# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/oneiot_core/websocket_helper.py
# Compiled at: 2020-01-26 17:26:32
# Size of source mod 2**32: 1595 bytes
import sys
try:
    import ubinascii as binascii
except:
    import binascii

try:
    import uhashlib as hashlib
except:
    import hashlib

DEBUG = 0

def server_handshake(sock):
    clr = sock.makefile('rwb', 0)
    l = clr.readline()
    webkey = None
    while 1:
        l = clr.readline()
        if not l:
            raise OSError('EOF in headers')
        if l == b'\r\n':
            break
        h, v = [x.strip() for x in l.split(b':', 1)]
        if DEBUG:
            print((h, v))
        if h == b'Sec-WebSocket-Key':
            webkey = v

    if not webkey:
        raise OSError('Not a websocket request')
    if DEBUG:
        print('Sec-WebSocket-Key:', webkey, len(webkey))
    respkey = webkey + b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    respkey = hashlib.sha1(respkey).digest()
    respkey = binascii.b2a_base64(respkey)[:-1]
    resp = b'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n' % respkey
    if DEBUG:
        print(resp)
    sock.send(resp)


def client_handshake(sock):
    cl = sock.makefile('rwb', 0)
    cl.write(b'GET / HTTP/1.1\r\nHost: echo.websocket.org\r\nConnection: Upgrade\r\nUpgrade: websocket\r\nSec-WebSocket-Key: foo\r\n\r\n')
    l = cl.readline()
    while 1:
        l = cl.readline()
        if l == b'\r\n':
            break