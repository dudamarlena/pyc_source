# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/pynexus/net.py
# Compiled at: 2016-08-31 07:58:37
# Size of source mod 2**32: 2830 bytes
import socket, srvlookup, ssl, websocket
ports = {'tcp':1717, 
 'ssl':1718, 
 'ws':80, 
 'wss':443}

def lookupSRV(hostname, scheme):
    try:
        return srvlookup.lookup('nexus', scheme, hostname)
    except:
        return []


def connect(hostname, port=None, scheme=None):
    if not scheme:
        scheme = 'ssl'
    else:
        if scheme == 'http':
            scheme = 'ws'
        if scheme == 'https':
            scheme = 'wss'
        servers = []
        if not port:
            addrs = lookupSRV(hostname, scheme)
            for addr in addrs:
                servers.append([addr.host, addr.port])
            else:
                servers.append([hostname, ports.get(scheme, 0)])
        else:
            servers.append([hostname, port])
        conn = None
        if scheme in ('tcp', 'ssl'):
            conn = create_tcp_connection(scheme, servers)
        elif scheme in ('ws', 'wss'):
            conn = create_ws_connection(scheme, servers)
    return conn


def create_tcp_connection(scheme, servers):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    error = None
    if scheme == 'ssl':
        conn = ssl.SSLSocket(conn)
    for hostname, port in servers:
        try:
            conn.connect((hostname, port))
            error = None
            break
        except Exception as e:
            try:
                error = e
            finally:
                e = None
                del e

    if error:
        raise error
    return conn


def create_ws_connection(scheme, servers):
    conn = None
    error = None
    for hostname, port in servers:
        try:
            conn = websocket.create_connection(('%s://%s:%s/' % (scheme, hostname, port)), sslopt={'cert_reqs': ssl.CERT_NONE})
            error = None
            break
        except Exception as e:
            try:
                error = e
            finally:
                e = None
                del e

    if error:
        raise error
    return conn