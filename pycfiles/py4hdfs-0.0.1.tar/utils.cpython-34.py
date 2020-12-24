# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.4/lib/python3.4/site-packages/org/py4grid/multicast/utils.py
# Compiled at: 2014-09-03 01:53:04
# Size of source mod 2**32: 3392 bytes
__doc__ = '\nPY4GRID : a little framework to simule multiprocessing over a lot of computers\nCopyright (C) 2014  João Jorge Pereira Farias Junior\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\nYou should have received a copy of the GNU General Public License\nalong with this program. If not, see <http://www.gnu.org/licenses/>.\n'
__author__ = 'dev'
import pickle, socket, struct, io, os, platform
MAX_BYTES = 16384

def loads2(by):
    return pickle.load(io.BytesIO(initial_bytes=by))


def dumps2(obj):
    return pickle.dumps(obj)


class QuitRequest:

    def __init__(self):
        self.pid = os.getpid()

    def __repr__(self):
        return 'QuitRequest(pid=' + str(self.pid) + ')'


class Request:

    def __init__(self):
        self.pid = os.getpid()

    def __repr__(self):
        return 'Request(pid=' + str(self.pid) + ')'


class Response:

    def __init__(self, hostname=None, port=None, ips=()):
        self.pid = os.getpid()
        self.hostname = hostname
        self.port = port
        self.ips = ips

    def __repr__(self):
        return 'Response(pid=' + str(self.pid) + ", hostname='" + self.hostname + "', ips=" + str(tuple(self.ips)) + ', port=' + str(self.port) + ')'


class MCastSocket:

    def __init__(self, mcasthost, mcastport):
        mreq = struct.pack('4sl', socket.inet_aton(mcasthost), socket.INADDR_ANY)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if platform.system() not in ('Windows', 'Linux') and hasattr(socket, 'SO_REUSEPORT'):
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.adr = (
         mcasthost, mcastport)
        self.sock.bind(('', mcastport))
        self.is_continue = True

    def __del__(self):
        self.sock.close()
        self.sock = None

    def send(self, obj):
        data = dumps2(obj)
        if len(data) > MAX_BYTES:
            raise Exception('too large msg')
        self.sock.sendto(data, self.adr)

    def stop(self):
        self.is_continue = False

    def recv(self):
        data = self.sock.recv(MAX_BYTES)
        return loads2(data)

    def __iter__(self):
        return self

    def __next__(self):
        msg = self.recv()
        if not isinstance(msg, QuitRequest) and self.is_continue:
            return msg
        raise StopIteration


QUIT_MSG = (-1, -1)
MCAST_SERVERS = '224.1.1.1'
MCAST_DISCOVER = '224.1.2.1'
MCAST_SERVERS_PORT = 50907
MCAST_DISCOVER_PORT = 50709

def getsocket(host, port):
    sock = MCastSocket(host, port)
    return sock