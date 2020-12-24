# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\VNDB\connection.py
# Compiled at: 2017-02-06 21:04:03
# Size of source mod 2**32: 4193 bytes
import socket, ujson
from ..errors import *
try:
    import ssl
except ImportError:
    raise NoSSL

class VNDBConnection:
    __doc__ = "\n    VNDB Connection Manager\n\n    :ivar dict clientvars: Needed for sending on login.\n    :ivar boolean loggedin: Are we logged in as a user?\n    :ivar bytes data_buffer: Low level sockets yo (Receive Buffer)\n    :ivar SSLContext sslcontet: SSLContext for the socket wrap\n    :ivar socket socket: The socket (It's imaginative naming)\n    :ivar regex helperpat: When queries are made on the server, this regex helps me build them correctly if the user doesn't\n    :raises: :class:`Pymoe.errors.NoSSL`\n    "

    def __init__(self, username=None, password=None):
        """
        Just a lowly connection handler for VNDB
        """
        self.clientvars = {'protocol':1, 
         'clientver':0.1,  'client':'Pymoe'}
        self.loggedin = False
        self.data_buffer = bytes(1024)
        self.sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.sslcontext.verify_mode = ssl.CERT_REQUIRED
        self.sslcontext.check_hostname = True
        self.sslcontext.load_default_certs()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sslwrap = self.sslcontext.wrap_socket((self.socket), server_hostname='api.vndb.org')
        self.sslwrap.connect(('api.vndb.org', 19535))
        self.login(username, password)

    def close(self):
        """
        Close the socket connection.

        :return: Nothing
        """
        self.sslwrap.close()

    def login(self, username, password):
        """
        This handles login logic instead of stuffing all that in the __init__.

        :param username: The username to log in as or None
        :param password: The password for that user or None
        :return: Nothing
        :raises: :class:`Pymoe.errors.UserLoginFailed` - Didn't respond with Ok
        :raises: :class:`Pymoe.errors.GeneralLoginError` - For some reason, we were already logged in, tried to login again and it failed. This probably isn't bad.
        """
        finvars = self.clientvars
        if username:
            if password:
                finvars['username'] = username
                finvars['password'] = password
                self.loggedin = True
                ret = self.send_command('login', ujson.dumps(finvars))
                if isinstance(ret, str) or self.loggedin:
                    self.loggedin = False
                    raise UserLoginFailed(ret['msg'])
            else:
                raise GeneralLoginError(ret['msg'])

    def send_command(self, command, args=None):
        """
        Send a command to VNDB and then get the result.

        :param command: What command are we sending
        :param args: What are the json args for this command
        :return: Servers Response
        :rtype: Dictionary (See D11 docs on VNDB)
        """
        if args:
            if isinstance(args, str):
                final_command = command + ' ' + args + '\x04'
            else:
                final_command = command + ' ' + ujson.dumps(args) + '\x04'
        else:
            final_command = command + '\x04'
        self.sslwrap.sendall(final_command.encode('utf-8'))
        return self._recv_data()

    def _recv_data(self):
        """
        Receieves data until we reach the \x04 and then returns it.

        :return: The data received
        """
        temp = ''
        while True:
            self.data_buffer = self.sslwrap.recv(1024)
            if '\x04' in self.data_buffer.decode('utf-8', 'ignore'):
                temp += self.data_buffer.decode('utf-8', 'ignore')
                break
            else:
                temp += self.data_buffer.decode('utf-8', 'ignore')
                self.data_buffer = bytes(1024)

        temp = temp.replace('\x04', '')
        if 'Ok' in temp:
            return temp
        else:
            return ujson.loads(temp.split(' ', 1)[1])