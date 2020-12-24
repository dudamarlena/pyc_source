# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/silva/pas/radius/radius.py
# Compiled at: 2008-11-20 12:49:45
"""
$Id: radius.py 32254 2008-11-20 15:52:07Z sylvain $

Extremly basic RADIUS authentication. Bare minimum required to authenticate
a user, yet remain RFC2138 compliant (I hope).

Homepage at http://py-radius.sourceforge.net
"""
from select import select
from struct import pack, unpack
from whrandom import randint, random
import md5, socket
__version__ = '1.0.1'
ACCESS_REQUEST = 1
ACCESS_ACCEPT = 2
ACCESSS_REJECT = 3
DEFAULT_RETRIES = 3
DEFAULT_TIMEOUT = 5

class Error(Exception):
    __module__ = __name__


class NoResponse(Error):
    __module__ = __name__


class SocketError(NoResponse):
    __module__ = __name__


def authenticate(username, password, secret, host='radius', port=1645):
    """Return 1 for a successful authentication. Other values indicate
       failure (should only ever be 0 anyway).

       Can raise either NoResponse or SocketError"""
    r = RADIUS(secret, host, port)
    return r.authenticate(username, password)


class RADIUS:
    __module__ = __name__

    def __init__(self, secret, host='radius', port=1645):
        self._secret = secret
        self._host = host
        self._port = port
        self.retries = DEFAULT_RETRIES
        self.timeout = DEFAULT_TIMEOUT
        self._socket = None
        return

    def __del__(self):
        self.closesocket()

    def opensocket(self):
        if self._socket == None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.connect((self._host, self._port))
        return

    def closesocket(self):
        if self._socket is not None:
            try:
                self._socket.close()
            except socket.error, x:
                raise SocketError(x)
            else:
                self._socket = None
        return

    def generateAuthenticator(self):
        """A 16 byte random string"""
        v = range(0, 17)
        v[0] = '16B'
        for i in range(1, 17):
            v[i] = randint(1, 255)

        return apply(pack, v)

    def radcrypt(self, authenticator, text, pad16=0):
        """Encrypt a password with the secret"""
        md5vec = md5.new(self._secret + authenticator).digest()
        r = ''
        for i in range(0, len(text)):
            if i % 16 == 0 and i != 0:
                md5vec = md5.new(self._secret + r[-16:]).digest()
            r = r + chr(ord(md5vec[i]) ^ ord(text[i]))

        if pad16:
            for i in range(len(r), 16):
                r = r + md5vec[i]

        return r

    def authenticate(self, uname, passwd):
        """Attempt t authenticate with the given username and password.
           Returns 0 on failure
           Returns 1 on success
           Raises a NoResponse (or its subclass SocketError) exception if
                no responses or no valid responses are received"""
        if not uname or not passwd:
            return 0
        try:
            self.opensocket()
            id = randint(0, 255)
            authenticator = self.generateAuthenticator()
            encpass = self.radcrypt(authenticator, passwd, 1)
            msg = pack('!B B H 16s B B %ds B B %ds' % (len(uname), len(encpass)), 1, id, len(uname) + len(encpass) + 24, authenticator, 1, len(uname) + 2, uname, 2, len(encpass) + 2, encpass)
            for i in range(0, self.retries):
                self._socket.send(msg)
                t = select([self._socket], [], [], self.timeout)
                if len(t[0]) > 0:
                    response = self._socket.recv(4096)
                else:
                    continue
                if ord(response[1]) != id:
                    continue
                checkauth = response[4:20]
                m = md5.new(response[0:4] + authenticator + response[20:] + self._secret).digest()
                if m != checkauth:
                    continue
                if ord(response[0]) == ACCESS_ACCEPT:
                    return 1
                else:
                    return 0

        except socket.error, x:
            try:
                self.closesocket()
            except:
                pass
            else:
                raise SocketError(x)

        raise NoResponse


Radius = RADIUS
if __name__ == '__main__':
    from getpass import getpass
    host = raw_input("Host? (default = 'radius')")
    port = raw_input('Port? (default = 1645) ')
    if not host:
        host = 'radius'
    if port:
        port = int(port)
    else:
        port = 1645
    secret = ''
    while not secret:
        secret = getpass('RADIUS Secret? ')

    r = RADIUS(secret, host, port)
    (uname, passwd) = (None, None)
    while not uname:
        uname = raw_input('Username? ')

    while not passwd:
        passwd = getpass('Password? ')

    if r.authenticate(uname, passwd):
        print 'Authentication Succeeded'
    else:
        print 'Authentication Failed'