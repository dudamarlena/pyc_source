# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/pk_common/common.py
# Compiled at: 2015-11-01 20:40:14
# Size of source mod 2**32: 1075 bytes
import hashlib, threading, socket
NUM_KNOCKS = 10
min_port, max_port = PORT_RANGE = (38000, 39000)

def mhash(s):
    return int.from_bytes(hashlib.md5(s.encode('utf8')).digest(), 'little')


def make_int(s):
    return int.from_bytes(s.encode('utf8'), 'little')


def _make_knocks(secret):
    return [_make_knock(secret, i) for i in range(NUM_KNOCKS)]


def _make_knock(secret, knock_ix):
    rsize = max_port - min_port
    return mhash(secret + str(knock_ix)) % rsize + min_port


def sock_open(host, port, localaddr=None):
    """
    Let clients pick local addr to reuse if they want for purpose of 
    firewalling hidden services by client addr
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if localaddr:
        sock.bind(localaddr)
    sock.connect((host, port))
    return sock


def on_thread(f, *args, **kwargs):
    t = threading.Thread(target=f, args=args, kwargs=kwargs)
    t.start()
    return t