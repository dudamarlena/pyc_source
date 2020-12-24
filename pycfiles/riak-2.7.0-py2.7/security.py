# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/transports/security.py
# Compiled at: 2016-10-17 19:06:50
"""
Copyright 2015 Basho Technologies, Inc.

This file is provided to you under the Apache License,
Version 2.0 (the "License"); you may not use this file
except in compliance with the License.  You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""
import socket
from riak.security import SecurityError, USE_STDLIB_SSL
if USE_STDLIB_SSL:
    import ssl
else:
    import OpenSSL.SSL
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

def verify_cb(conn, cert, errnum, depth, ok):
    """
    The default OpenSSL certificate verification callback.
    """
    if not ok:
        raise SecurityError(('Could not verify CA certificate {0}').format(cert.get_subject()))
    return ok


if USE_STDLIB_SSL:

    def configure_ssl_context(credentials):
        """
        Set various options on the SSL context for Python >= 2.7.9 and 3.x.

        N.B. versions earlier than 3.4 may not support all security
        measures, e.g., hostname check.

        :param credentials: Riak Security Credentials
        :type credentials: :class:`~riak.security.SecurityCreds`
        :rtype :class:`~ssl.SSLContext`
        """
        ssl_ctx = ssl.SSLContext(credentials.ssl_version)
        ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        if hasattr(ssl_ctx, 'check_hostname'):
            ssl_ctx.check_hostname = True
        if credentials.cacert_file is None:
            raise SecurityError('cacert_file is required in SecurityCreds')
        if credentials.ciphers is not None:
            ssl_ctx.set_ciphers(credentials.ciphers)
        ssl_ctx.load_verify_locations(credentials.cacert_file)
        if credentials.ciphers is not None:
            ssl_ctx.set_ciphers(credentials.ciphers)
        pkeyfile = credentials.pkey_file
        certfile = credentials.cert_file
        if pkeyfile and not certfile:
            raise SecurityError('cert_file must be specified with pkey_file')
        if certfile and not pkeyfile:
            pkeyfile = certfile
        if certfile:
            ssl_ctx.load_cert_chain(certfile, pkeyfile)
        if credentials.crl_file is not None:
            ssl_ctx.load_verify_locations(credentials.crl_file)
            ssl_ctx.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
        ssl_ctx.options |= ssl.OP_NO_SSLv2
        ssl_ctx.options |= ssl.OP_NO_SSLv3
        ssl_ctx.options |= ssl.OP_NO_COMPRESSION
        return ssl_ctx


else:

    def configure_pyopenssl_context(credentials):
        """
        Set various options on the SSL context for Python <= 2.7.8.

        :param credentials: Riak Security Credentials
        :type credentials: :class:`~riak.security.SecurityCreds`
        :rtype ssl_ctx: :class:`~OpenSSL.SSL.Context`
        """
        ssl_ctx = OpenSSL.SSL.Context(credentials.ssl_version)
        if credentials._has_credential('pkey'):
            ssl_ctx.use_privatekey(credentials.pkey)
        if credentials._has_credential('cert'):
            ssl_ctx.use_certificate(credentials.cert)
        if credentials._has_credential('cacert'):
            store = ssl_ctx.get_cert_store()
            cacerts = credentials.cacert
            if not isinstance(cacerts, list):
                cacerts = [
                 cacerts]
            for cacert in cacerts:
                store.add_cert(cacert)

        else:
            raise SecurityError('cacert_file is required in SecurityCreds')
        ciphers = credentials.ciphers
        if ciphers is not None:
            ssl_ctx.set_cipher_list(ciphers)
        ssl_ctx.set_verify(OpenSSL.SSL.VERIFY_PEER | OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_cb)
        return ssl_ctx


    class RiakWrappedSocket(socket.socket):

        def __init__(self, connection, socket):
            """
            API-compatibility wrapper for Python OpenSSL's Connection-class.

            :param connection: OpenSSL connection
            :type connection: OpenSSL.SSL.Connection
            :param socket: Underlying already connected socket
            :type socket: socket
            """
            self.connection = connection
            self.socket = socket

        def fileno(self):
            return self.socket.fileno()

        def makefile(self, mode, bufsize=-1):
            return fileobject(self.connection, mode, bufsize)

        def settimeout(self, timeout):
            return self.socket.settimeout(timeout)

        def sendall(self, data):
            return self.connection.sendall(bytes(data))

        def close(self):
            try:
                return self.connection.shutdown()
            except OpenSSL.SSL.Error as err:
                if err.args == ([],):
                    return False
                raise err


    class fileobject(socket._fileobject):
        """
        Extension of the socket module's fileobject to use PyOpenSSL.
        """

        def read(self, size=-1):
            rbufsize = max(self._rbufsize, self.default_bufsize)
            buf = self._rbuf
            buf.seek(0, 2)
            if size < 0:
                self._rbuf = StringIO()
                while True:
                    try:
                        data = self._sock.recv(rbufsize)
                    except OpenSSL.SSL.WantReadError:
                        continue

                    if not data:
                        break
                    buf.write(data)

                return buf.getvalue()
            else:
                buf_len = buf.tell()
                if buf_len >= size:
                    buf.seek(0)
                    rv = buf.read(size)
                    self._rbuf = StringIO()
                    self._rbuf.write(buf.read())
                    return rv
                self._rbuf = StringIO()
                while True:
                    left = size - buf_len
                    try:
                        data = self._sock.recv(left)
                    except OpenSSL.SSL.WantReadError:
                        continue

                    if not data:
                        break
                    n = len(data)
                    if n == size and not buf_len:
                        return data
                    if n == left:
                        buf.write(data)
                        break
                    assert n <= left, 'recv(%d) returned %d bytes' % (left, n)
                    buf.write(data)
                    buf_len += n

                if data:
                    del data
                return buf.getvalue()

        def readline(self, size=-1):
            data = None
            buf = self._rbuf
            buf.seek(0, 2)
            if buf.tell() > 0:
                buf.seek(0)
                bline = buf.readline(size)
                if bline.endswith('\n') or len(bline) == size:
                    self._rbuf = StringIO()
                    self._rbuf.write(buf.read())
                    return bline
                del bline
            if size < 0:
                if self._rbufsize <= 1:
                    buf.seek(0)
                    buffers = [buf.read()]
                    self._rbuf = StringIO()
                    data = None
                    recv = self._sock.recv
                    while True:
                        try:
                            while data != '\n':
                                data = recv(1)
                                if not data:
                                    break
                                buffers.append(data)

                        except OpenSSL.SSL.WantReadError:
                            continue

                        break

                    return ('').join(buffers)
                buf.seek(0, 2)
                self._rbuf = StringIO()
                while True:
                    try:
                        data = self._sock.recv(self._rbufsize)
                    except OpenSSL.SSL.WantReadError:
                        continue

                    if not data:
                        break
                    nl = data.find('\n')
                    if nl >= 0:
                        nl += 1
                        buf.write(data[:nl])
                        self._rbuf.write(data[nl:])
                        break
                    buf.write(data)

                if data:
                    del data
                return buf.getvalue()
            else:
                buf.seek(0, 2)
                buf_len = buf.tell()
                if buf_len >= size:
                    buf.seek(0)
                    rv = buf.read(size)
                    self._rbuf = StringIO()
                    self._rbuf.write(buf.read())
                    return rv
                self._rbuf = StringIO()
                while True:
                    try:
                        data = self._sock.recv(self._rbufsize)
                    except OpenSSL.SSL.WantReadError:
                        continue

                    if not data:
                        break
                    left = size - buf_len
                    nl = data.find('\n', 0, left)
                    if nl >= 0:
                        nl += 1
                        self._rbuf.write(data[nl:])
                        if buf_len:
                            buf.write(data[:nl])
                            break
                        else:
                            return data[:nl]
                    n = len(data)
                    if n == size and not buf_len:
                        return data
                    if n >= left:
                        buf.write(data[:left])
                        self._rbuf.write(data[left:])
                        break
                    buf.write(data)
                    buf_len += n

                return buf.getvalue()
                return