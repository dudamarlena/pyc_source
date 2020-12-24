# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\network.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 19202 bytes
"""Module implementing low-level socket communication with MySQL servers.
"""
from collections import deque
import socket, struct, sys, zlib
try:
    import ssl
except:
    pass

from . import constants, errors
from .catch23 import PY2, init_bytearray, struct_unpack

def _strioerror(err):
    """Reformat the IOError error message

    This function reformats the IOError error message.
    """
    if not err.errno:
        return str(err)
    else:
        return '{errno} {strerr}'.format(errno=(err.errno), strerr=(err.strerror))


def _prepare_packets(buf, pktnr):
    """Prepare a packet for sending to the MySQL server"""
    pkts = []
    pllen = len(buf)
    maxpktlen = constants.MAX_PACKET_LENGTH
    while pllen > maxpktlen:
        pkts.append(b'\xff\xff\xff' + struct.pack('<B', pktnr) + buf[:maxpktlen])
        buf = buf[maxpktlen:]
        pllen = len(buf)
        pktnr = pktnr + 1

    pkts.append(struct.pack('<I', pllen)[0:3] + struct.pack('<B', pktnr) + buf)
    return pkts


class BaseMySQLSocket(object):
    __doc__ = 'Base class for MySQL socket communication\n\n    This class should not be used directly but overloaded, changing the\n    at least the open_connection()-method. Examples of subclasses are\n      mysql.connector.network.MySQLTCPSocket\n      mysql.connector.network.MySQLUnixSocket\n    '

    def __init__(self):
        self.sock = None
        self._connection_timeout = None
        self._packet_number = -1
        self._compressed_packet_number = -1
        self._packet_queue = deque()
        self.recvsize = 8192

    @property
    def next_packet_number(self):
        """Increments the packet number"""
        self._packet_number = self._packet_number + 1
        if self._packet_number > 255:
            self._packet_number = 0
        return self._packet_number

    @property
    def next_compressed_packet_number(self):
        """Increments the compressed packet number"""
        self._compressed_packet_number = self._compressed_packet_number + 1
        if self._compressed_packet_number > 255:
            self._compressed_packet_number = 0
        return self._compressed_packet_number

    def open_connection(self):
        """Open the socket"""
        raise NotImplementedError

    def get_address(self):
        """Get the location of the socket"""
        raise NotImplementedError

    def shutdown(self):
        """Shut down the socket before closing it"""
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            del self._packet_queue
        except (socket.error, AttributeError):
            pass

    def close_connection(self):
        """Close the socket"""
        try:
            self.sock.close()
            del self._packet_queue
        except (socket.error, AttributeError):
            pass

    def send_plain(self, buf, packet_number=None, compressed_packet_number=None):
        """Send packets to the MySQL server"""
        if packet_number is None:
            self.next_packet_number
        else:
            self._packet_number = packet_number
        packets = _prepare_packets(buf, self._packet_number)
        for packet in packets:
            try:
                if PY2:
                    self.sock.sendall(buffer(packet))
                else:
                    self.sock.sendall(packet)
            except IOError as err:
                raise errors.OperationalError(errno=2055,
                  values=(self.get_address(), _strioerror(err)))
            except AttributeError:
                raise errors.OperationalError(errno=2006)

    send = send_plain

    def send_compressed(self, buf, packet_number=None, compressed_packet_number=None):
        """Send compressed packets to the MySQL server"""
        if packet_number is None:
            self.next_packet_number
        else:
            self._packet_number = packet_number
        if compressed_packet_number is None:
            self.next_compressed_packet_number
        else:
            self._compressed_packet_number = compressed_packet_number
        pktnr = self._packet_number
        pllen = len(buf)
        zpkts = []
        maxpktlen = constants.MAX_PACKET_LENGTH
        if pllen > maxpktlen:
            pkts = _prepare_packets(buf, pktnr)
            if PY2:
                tmpbuf = bytearray()
                for pkt in pkts:
                    tmpbuf += pkt

                tmpbuf = buffer(tmpbuf)
            else:
                tmpbuf = (b'').join(pkts)
            del pkts
            zbuf = zlib.compress(tmpbuf[:16384])
            header = struct.pack('<I', len(zbuf))[0:3] + struct.pack('<B', self._compressed_packet_number) + b'\x00@\x00'
            if PY2:
                header = buffer(header)
            zpkts.append(header + zbuf)
            tmpbuf = tmpbuf[16384:]
            pllen = len(tmpbuf)
            self.next_compressed_packet_number
            while pllen > maxpktlen:
                zbuf = zlib.compress(tmpbuf[:maxpktlen])
                header = struct.pack('<I', len(zbuf))[0:3] + struct.pack('<B', self._compressed_packet_number) + b'\xff\xff\xff'
                if PY2:
                    header = buffer(header)
                zpkts.append(header + zbuf)
                tmpbuf = tmpbuf[maxpktlen:]
                pllen = len(tmpbuf)
                self.next_compressed_packet_number

            if tmpbuf:
                zbuf = zlib.compress(tmpbuf)
                header = struct.pack('<I', len(zbuf))[0:3] + struct.pack('<B', self._compressed_packet_number) + struct.pack('<I', pllen)[0:3]
                if PY2:
                    header = buffer(header)
                zpkts.append(header + zbuf)
            del tmpbuf
        else:
            pkt = struct.pack('<I', pllen)[0:3] + struct.pack('<B', pktnr) + buf
            if PY2:
                pkt = buffer(pkt)
            pllen = len(pkt)
        if pllen > 50:
            zbuf = zlib.compress(pkt)
            zpkts.append(struct.pack('<I', len(zbuf))[0:3] + struct.pack('<B', self._compressed_packet_number) + struct.pack('<I', pllen)[0:3] + zbuf)
        else:
            header = struct.pack('<I', pllen)[0:3] + struct.pack('<B', self._compressed_packet_number) + struct.pack('<I', 0)[0:3]
            if PY2:
                header = buffer(header)
            zpkts.append(header + pkt)
        for zip_packet in zpkts:
            try:
                self.sock.sendall(zip_packet)
            except IOError as err:
                raise errors.OperationalError(errno=2055,
                  values=(self.get_address(), _strioerror(err)))
            except AttributeError:
                raise errors.OperationalError(errno=2006)

    def recv_plain(self):
        """Receive packets from the MySQL server"""
        try:
            packet = bytearray(b'')
            packet_len = 0
            while packet_len < 4:
                chunk = self.sock.recv(4 - packet_len)
                if not chunk:
                    raise errors.InterfaceError(errno=2013)
                packet += chunk
                packet_len = len(packet)

            self._packet_number = packet[3]
            if PY2:
                payload_len = struct.unpack_from('<I', buffer(packet[0:3] + b'\x00'))[0]
            else:
                payload_len = struct.unpack('<I', packet[0:3] + b'\x00')[0]
            rest = payload_len
            packet.extend(bytearray(payload_len))
            packet_view = memoryview(packet)
            packet_view = packet_view[4:]
            while rest:
                read = self.sock.recv_into(packet_view, rest)
                if read == 0:
                    if rest > 0:
                        raise errors.InterfaceError(errno=2013)
                packet_view = packet_view[read:]
                rest -= read

            return packet
        except IOError as err:
            raise errors.OperationalError(errno=2055,
              values=(self.get_address(), _strioerror(err)))

    def recv_py26_plain(self):
        """Receive packets from the MySQL server"""
        try:
            header = bytearray(b'')
            header_len = 0
            while header_len < 4:
                chunk = self.sock.recv(4 - header_len)
                if not chunk:
                    raise errors.InterfaceError(errno=2013)
                header += chunk
                header_len = len(header)

            self._packet_number = header[3]
            payload_len = struct_unpack('<I', header[0:3] + b'\x00')[0]
            rest = payload_len
            payload = init_bytearray(b'')
            while rest > 0:
                chunk = self.sock.recv(rest)
                if not chunk:
                    raise errors.InterfaceError(errno=2013)
                payload += chunk
                rest = payload_len - len(payload)

            return header + payload
        except IOError as err:
            raise errors.OperationalError(errno=2055,
              values=(self.get_address(), _strioerror(err)))

    if sys.version_info[0:2] == (2, 6):
        recv = recv_py26_plain
        recv_plain = recv_py26_plain
    else:
        recv = recv_plain

    def _split_zipped_payload(self, packet_bunch):
        """Split compressed payload"""
        while packet_bunch:
            if PY2:
                payload_length = struct.unpack_from('<I', packet_bunch[0:3] + b'\x00')[0]
            else:
                payload_length = struct.unpack('<I', packet_bunch[0:3] + b'\x00')[0]
            self._packet_queue.append(packet_bunch[0:payload_length + 4])
            packet_bunch = packet_bunch[payload_length + 4:]

    def recv_compressed(self):
        """Receive compressed packets from the MySQL server"""
        try:
            pkt = self._packet_queue.popleft()
            self._packet_number = pkt[3]
            return pkt
        except IndexError:
            pass

        header = bytearray(b'')
        packets = []
        try:
            abyte = self.sock.recv(1)
            while abyte and len(header) < 7:
                header += abyte
                abyte = self.sock.recv(1)

            while header:
                if len(header) < 7:
                    raise errors.InterfaceError(errno=2013)
                else:
                    zip_payload_length = struct_unpack('<I', header[0:3] + b'\x00')[0]
                    self._compressed_packet_number = header[3]
                    payload_length = struct_unpack('<I', header[4:7] + b'\x00')[0]
                    zip_payload = init_bytearray(abyte)
                    while len(zip_payload) < zip_payload_length:
                        chunk = self.sock.recv(zip_payload_length - len(zip_payload))
                        if len(chunk) == 0:
                            raise errors.InterfaceError(errno=2013)
                        zip_payload = zip_payload + chunk

                    if payload_length == 0:
                        self._split_zipped_payload(zip_payload)
                        pkt = self._packet_queue.popleft()
                        self._packet_number = pkt[3]
                        return pkt
                    packets.append((payload_length, zip_payload))
                    if zip_payload_length <= 16384:
                        break
                header = init_bytearray(b'')
                abyte = self.sock.recv(1)
                while abyte and len(header) < 7:
                    header += abyte
                    abyte = self.sock.recv(1)

        except IOError as err:
            raise errors.OperationalError(errno=2055,
              values=(self.get_address(), _strioerror(err)))

        tmp = init_bytearray(b'')
        for payload_length, payload in packets:
            if PY2:
                tmp += zlib.decompress(buffer(payload))
            else:
                tmp += zlib.decompress(payload)

        self._split_zipped_payload(tmp)
        del tmp
        try:
            pkt = self._packet_queue.popleft()
            self._packet_number = pkt[3]
            return pkt
        except IndexError:
            pass

    def set_connection_timeout(self, timeout):
        """Set the connection timeout"""
        self._connection_timeout = timeout

    def switch_to_ssl(self, ca, cert, key, verify_cert=False, cipher=None):
        """Switch the socket to use SSL"""
        if not self.sock:
            raise errors.InterfaceError(errno=2048)
        try:
            if verify_cert:
                cert_reqs = ssl.CERT_REQUIRED
            else:
                cert_reqs = ssl.CERT_NONE
            self.sock = ssl.wrap_socket((self.sock),
              keyfile=key, certfile=cert, ca_certs=ca, cert_reqs=cert_reqs,
              do_handshake_on_connect=False,
              ssl_version=(ssl.PROTOCOL_TLSv1),
              ciphers=cipher)
            self.sock.do_handshake()
        except NameError:
            raise errors.NotSupportedError('Python installation has no SSL support')
        except (ssl.SSLError, IOError) as err:
            raise errors.InterfaceError(errno=2055,
              values=(self.get_address(), _strioerror(err)))
        except NotImplementedError as err:
            raise errors.InterfaceError(str(err))


class MySQLUnixSocket(BaseMySQLSocket):
    __doc__ = 'MySQL socket class using UNIX sockets\n\n    Opens a connection through the UNIX socket of the MySQL Server.\n    '

    def __init__(self, unix_socket='/tmp/mysql.sock'):
        super(MySQLUnixSocket, self).__init__()
        self.unix_socket = unix_socket

    def get_address(self):
        return self.unix_socket

    def open_connection(self):
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.settimeout(self._connection_timeout)
            self.sock.connect(self.unix_socket)
        except IOError as err:
            raise errors.InterfaceError(errno=2002,
              values=(self.get_address(), _strioerror(err)))
        except Exception as err:
            raise errors.InterfaceError(str(err))


class MySQLTCPSocket(BaseMySQLSocket):
    __doc__ = 'MySQL socket class using TCP/IP\n\n    Opens a TCP/IP connection to the MySQL Server.\n    '

    def __init__(self, host='127.0.0.1', port=3306, force_ipv6=False):
        super(MySQLTCPSocket, self).__init__()
        self.server_host = host
        self.server_port = port
        self.force_ipv6 = force_ipv6
        self._family = 0

    def get_address(self):
        return '{0}:{1}'.format(self.server_host, self.server_port)

    def open_connection(self):
        """Open the TCP/IP connection to the MySQL server
        """
        addrinfo = [
         None] * 5
        try:
            addrinfos = socket.getaddrinfo(self.server_host, self.server_port, 0, socket.SOCK_STREAM, socket.SOL_TCP)
            for info in addrinfos:
                if self.force_ipv6 and info[0] == socket.AF_INET6:
                    addrinfo = info
                    break
                elif info[0] == socket.AF_INET:
                    addrinfo = info
                    break

            if self.force_ipv6:
                if addrinfo[0] is None:
                    raise errors.InterfaceError('No IPv6 address found for {0}'.format(self.server_host))
            if addrinfo[0] is None:
                addrinfo = addrinfos[0]
        except IOError as err:
            raise errors.InterfaceError(errno=2003,
              values=(self.get_address(), _strioerror(err)))
        else:
            self._family, socktype, proto, _, sockaddr = addrinfo
        try:
            self.sock = socket.socket(self._family, socktype, proto)
            self.sock.settimeout(self._connection_timeout)
            self.sock.connect(sockaddr)
        except IOError as err:
            raise errors.InterfaceError(errno=2003,
              values=(self.get_address(), _strioerror(err)))
        except Exception as err:
            raise errors.OperationalError(str(err))