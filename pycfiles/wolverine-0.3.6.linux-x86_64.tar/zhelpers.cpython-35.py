# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/wolverine/module/controller/zhelpers.py
# Compiled at: 2015-10-19 17:47:00
# Size of source mod 2**32: 2350 bytes
"""
Helper module for example applications. Mimics ZeroMQ Guide's zhelpers.h.
"""
from __future__ import print_function
import binascii, logging, msgpack, os
from random import randint
import zmq
logger = logging.getLogger(__name__)

def dump(msg_or_socket):
    out = '\n-------data-packet-------'
    if isinstance(msg_or_socket, zmq.Socket):
        msg = msg_or_socket.recv_multipart()
    else:
        msg = msg_or_socket
    for part in msg:
        out += '\n[%03d] ' % len(part)
        try:
            out += part.decode('utf-8')
        except UnicodeDecodeError:
            try:
                out += str(msgpack.unpackb(part))
            except Exception:
                out += '0x%s' % binascii.hexlify(part).decode('ascii')

    out += '\n' + '-' * 25
    logger.debug(out)


def packb(data):
    try:
        return msgpack.packb(data, use_bin_type=True)
    except Exception:
        logger.error('error packing data', extra={'data': data}, exc_info=True)


def unpack(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return unpackb(data)


def unpackb(data):
    try:
        return msgpack.unpackb(data, encoding='utf-8')
    except Exception:
        logger.warning("couldn't decode data" + str(data))
        return data


def set_id(zsocket):
    """Set simple random printable identity on socket"""
    identity = '%04x-%04x' % (randint(0, 65536), randint(0, 65536))
    zsocket.setsockopt_string(zmq.IDENTITY, identity)


def zpipe(ctx):
    """build inproc pipe for talking to threads

    mimic pipe used in czmq zthread_fork.

    Returns a pair of PAIRs connected via inproc
    """
    a = ctx.socket(zmq.PAIR)
    b = ctx.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    iface = 'inproc://%s' % binascii.hexlify(os.urandom(8))
    a.bind(iface)
    b.connect(iface)
    return (a, b)


ZMQ_EVENTS = {getattr(zmq, name):name.replace('EVENT_', '').lower().replace('_', ' ') for name in [i for i in dir(zmq) if i.startswith('EVENT_')]}

def event_description(event):
    """ Return a human readable description of the event """
    return ZMQ_EVENTS.get(event, 'unknown')