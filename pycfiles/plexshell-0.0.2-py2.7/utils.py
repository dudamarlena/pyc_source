# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/plexshell/utils.py
# Compiled at: 2011-09-17 18:35:43
from httplib import MOVED_PERMANENTLY, OK
import sys

class PlexError(Exception):
    """ Exception raised when a server error is detected """
    pass


class Colors:
    Blue = '\x1b[94m'
    Green = '\x1b[92m'
    Red = '\x1b[91m'
    EndC = '\x1b[0m'


def colorize(string, color):
    return color + string + Colors.EndC


def parse_address(address, connection):
    if not address.startswith('http://'):
        return (connection.host, connection.port, address)
    address = address.replace('http://', '')
    host, port = address.split('/')[0].split(':')
    return (host, port, address.replace('%s:%s' % (host, port), ''))


def chunked_read(response, chunk_size=4096, progress=False):
    result = ''
    bytes_read = 0
    while True:
        chunk = response.read(chunk_size)
        bytes_read += len(chunk)
        result += chunk
        if progress:
            sys.stdout.write('\rread: %s bytes' % bytes_read)
            sys.stdout.flush()
        if not chunk:
            break

    return result


def get(conn, path, error_msg, progress=False):
    conn.request('GET', path)
    response = conn.getresponse()
    if response.status == MOVED_PERMANENTLY:
        location = response.getheader('location')
        print 'redirected: %s' % location
        host, port, address = parse_address(location, conn)
        conn = HTTPConnection(host, port)
        return get(conn, address, error_msg, progress=progress)
    else:
        if not response.status == OK:
            if error_msg:
                print '%s: %s' % (error_msg, response.reason)
            return None
        return chunked_read(response, progress=progress)