# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/oneiot_core/webrepl_cli.py
# Compiled at: 2020-01-26 17:26:32
# Size of source mod 2**32: 6554 bytes
from __future__ import print_function
import sys, os, struct
try:
    import usocket as socket
except ImportError:
    import socket

import websocket_helper
USE_BUILTIN_UWEBSOCKET = 0
SANDBOX = ''
DEBUG = 0
WEBREPL_REQ_S = '<2sBBQLH64s'
WEBREPL_PUT_FILE = 1
WEBREPL_GET_FILE = 2
WEBREPL_GET_VER = 3

def debugmsg(msg):
    if DEBUG:
        print(msg)


if USE_BUILTIN_UWEBSOCKET:
    from uwebsocket import websocket
else:

    class websocket:

        def __init__(self, s):
            self.s = s
            self.buf = b''

        def write(self, data):
            l = len(data)
            if l < 126:
                hdr = struct.pack('>BB', 130, l)
            else:
                hdr = struct.pack('>BBH', 130, 126, l)
            self.s.send(hdr)
            self.s.send(data)

        def recvexactly(self, sz):
            res = b''
            while sz:
                data = self.s.recv(sz)
                if not data:
                    break
                res += data
                sz -= len(data)

            return res

        def read(self, size, text_ok=False):
            if not self.buf:
                while 1:
                    hdr = self.recvexactly(2)
                    assert len(hdr) == 2
                    fl, sz = struct.unpack('>BB', hdr)
                    if sz == 126:
                        hdr = self.recvexactly(2)
                        assert len(hdr) == 2
                        sz, = struct.unpack('>H', hdr)
                    if fl == 130:
                        break
                    if text_ok:
                        if fl == 129:
                            break
                    debugmsg('Got unexpected websocket record of type %x, skipping it' % fl)
                    while sz:
                        skip = self.s.recv(sz)
                        debugmsg('Skip data: %s' % skip)
                        sz -= len(skip)

                data = self.recvexactly(sz)
                assert len(data) == sz
                self.buf = data
            d = self.buf[:size]
            self.buf = self.buf[size:]
            assert len(d) == size, len(d)
            return d

        def ioctl(self, req, val):
            if not (req == 9 and val == 2):
                raise AssertionError


def login(ws, passwd):
    while 1:
        c = ws.read(1, text_ok=True)
        if c == b':':
            assert ws.read(1, text_ok=True) == b' '
            break

    ws.write(passwd.encode('utf-8') + b'\r')


def read_resp(ws):
    data = ws.read(4)
    sig, code = struct.unpack('<2sH', data)
    assert sig == b'WB'
    return code


def send_req(ws, op, sz=0, fname=b''):
    rec = struct.pack(WEBREPL_REQ_S, b'WA', op, 0, 0, sz, len(fname), fname)
    debugmsg('%r %d' % (rec, len(rec)))
    ws.write(rec)


def get_ver(ws):
    send_req(ws, WEBREPL_GET_VER)
    d = ws.read(3)
    d = struct.unpack('<BBB', d)
    return d


def put_file(ws, local_file, remote_file):
    sz = os.stat(local_file)[6]
    dest_fname = (SANDBOX + remote_file).encode('utf-8')
    rec = struct.pack(WEBREPL_REQ_S, b'WA', WEBREPL_PUT_FILE, 0, 0, sz, len(dest_fname), dest_fname)
    debugmsg('%r %d' % (rec, len(rec)))
    ws.write(rec[:10])
    ws.write(rec[10:])
    assert read_resp(ws) == 0
    cnt = 0
    with open(local_file, 'rb') as (f):
        while True:
            sys.stdout.write('Sent %d of %d bytes\r' % (cnt, sz))
            sys.stdout.flush()
            buf = f.read(1024)
            if not buf:
                break
            ws.write(buf)
            cnt += len(buf)

    print()
    assert read_resp(ws) == 0


def get_file(ws, local_file, remote_file):
    src_fname = (SANDBOX + remote_file).encode('utf-8')
    rec = struct.pack(WEBREPL_REQ_S, b'WA', WEBREPL_GET_FILE, 0, 0, 0, len(src_fname), src_fname)
    debugmsg('%r %d' % (rec, len(rec)))
    ws.write(rec)
    assert read_resp(ws) == 0
    with open(local_file, 'wb') as (f):
        cnt = 0
        while 1:
            ws.write(b'\x00')
            sz, = struct.unpack('<H', ws.read(2))
            if sz == 0:
                break
            while sz:
                buf = ws.read(sz)
                if not buf:
                    raise OSError()
                cnt += len(buf)
                f.write(buf)
                sz -= len(buf)
                sys.stdout.write('Received %d bytes\r' % cnt)
                sys.stdout.flush()

    print()
    assert read_resp(ws) == 0


def help(rc=0):
    exename = sys.argv[0].rsplit('/', 1)[(-1)]
    print('%s - Perform remote file operations using MicroPython WebREPL protocol' % exename)
    print('Arguments:')
    print('  [-p password] <host>:<remote_file> <local_file> - Copy remote file to local file')
    print('  [-p password] <local_file> <host>:<remote_file> - Copy local file to remote file')
    print('Examples:')
    print('  %s script.py 192.168.4.1:/another_name.py' % exename)
    print('  %s script.py 192.168.4.1:/app/' % exename)
    print('  %s -p password 192.168.4.1:/app/script.py .' % exename)
    sys.exit(rc)


def error(msg):
    print(msg)
    sys.exit(1)


def parse_remote(remote):
    host, fname = remote.rsplit(':', 1)
    if fname == '':
        fname = '/'
    port = 8266
    if ':' in host:
        host, port = host.split(':')
        port = int(port)
    return (
     host, port, fname)


def main(passwd, remote, op, dst_file=None, src_file=None):
    if op == 'get':
        host, port, src_file = parse_remote(remote)
        if os.path.isdir(dst_file):
            basename = src_file.rsplit('/', 1)[(-1)]
            dst_file += '/' + basename
    else:
        host, port, dst_file = parse_remote(remote)
        if dst_file[(-1)] == '/':
            basename = src_file.rsplit('/', 1)[(-1)]
            dst_file += basename
    print('op:%s, host:%s, port:%d, passwd:%s.' % (op, host, port, passwd))
    print(src_file, '->', dst_file)
    s = socket.socket()
    ai = socket.getaddrinfo(host, port)
    addr = ai[0][4]
    s.connect(addr)
    websocket_helper.client_handshake(s)
    ws = websocket(s)
    login(ws, passwd)
    print('Remote WebREPL version:', get_ver(ws))
    ws.ioctl(9, 2)
    if op == 'get':
        get_file(ws, dst_file, src_file)
    else:
        if op == 'put':
            put_file(ws, src_file, dst_file)
        s.close()