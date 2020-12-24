# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\lib\sourcelib\SourceRcon.py
# Compiled at: 2013-02-18 23:04:31
"""http://developer.valvesoftware.com/wiki/Source_RCON_Protocol"""
import select, socket, struct
SERVERDATA_AUTH = 3
SERVERDATA_AUTH_RESPONSE = 2
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_RESPONSE_VALUE = 0
MAX_COMMAND_LENGTH = 510
MIN_MESSAGE_LENGTH = 10
MAX_MESSAGE_LENGTH = 4105
PROBABLY_SPLIT_IF_LARGER_THAN = MAX_MESSAGE_LENGTH - 400

class SourceRconError(Exception):
    pass


class SourceRcon(object):
    """Example usage:

       import SourceRcon
       server = SourceRcon.SourceRcon('1.2.3.4', 27015, 'secret')
       print server.rcon('cvarlist')
    """

    def __init__(self, host, port=27015, password='', timeout=1.0):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self.tcp = False
        self.reqid = 0

    def disconnect(self):
        """Disconnect from the server."""
        if self.tcp:
            self.tcp.close()

    def connect(self):
        """Connect to the server. Should only be used internally."""
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.settimeout(self.timeout)
        self.tcp.connect((self.host, self.port))

    def send(self, cmd, message):
        """Send command and message to the server. Should only be used internally."""
        if len(message) > MAX_COMMAND_LENGTH:
            raise SourceRconError('RCON message too large to send')
        self.reqid += 1
        data = struct.pack('<l', self.reqid) + struct.pack('<l', cmd) + message + '\x00\x00'
        self.tcp.send(struct.pack('<l', len(data)) + data)

    def receive(self):
        """Receive a reply from the server. Should only be used internally."""
        packetsize = False
        requestid = False
        response = False
        message = ''
        message2 = ''
        while 1:
            buf = ''
            while len(buf) < 4:
                try:
                    recv = self.tcp.recv(4 - len(buf))
                    if not len(recv):
                        raise SourceRconError('RCON connection unexpectedly closed by remote host')
                    buf += recv
                except SourceRconError:
                    raise
                except:
                    break

            if len(buf) != 4:
                break
            packetsize = struct.unpack('<l', buf)[0]
            if packetsize < MIN_MESSAGE_LENGTH or packetsize > MAX_MESSAGE_LENGTH:
                raise SourceRconError('RCON packet claims to have illegal size: %d bytes' % (packetsize,))
            buf = ''
            while len(buf) < packetsize:
                try:
                    recv = self.tcp.recv(packetsize - len(buf))
                    if not len(recv):
                        raise SourceRconError('RCON connection unexpectedly closed by remote host')
                    buf += recv
                except SourceRconError:
                    raise
                except:
                    break

            if len(buf) != packetsize:
                raise SourceRconError('Received RCON packet with bad length (%d of %d bytes)' % (len(buf), packetsize))
            requestid = struct.unpack('<l', buf[:4])[0]
            if requestid == -1:
                self.disconnect()
                raise SourceRconError('Bad RCON password')
            else:
                if requestid != self.reqid:
                    raise SourceRconError('RCON request id error: %d, expected %d' % (requestid, self.reqid))
                response = struct.unpack('<l', buf[4:8])[0]
                if response == SERVERDATA_AUTH_RESPONSE:
                    return True
            if response != SERVERDATA_RESPONSE_VALUE:
                raise SourceRconError('Invalid RCON command response: %d' % (response,))
            str1 = buf[8:]
            pos1 = str1.index('\x00')
            str2 = str1[pos1 + 1:]
            pos2 = str2.index('\x00')
            crap = str2[pos2 + 1:]
            if crap:
                raise SourceRconError('RCON response contains %d superfluous bytes' % (len(crap),))
            message += str1[:pos1]
            message2 += str2[:pos2]
            poll = select.select([self.tcp], [], [], 0)
            if not len(poll[0]) and packetsize < PROBABLY_SPLIT_IF_LARGER_THAN:
                break

        if response is False:
            raise SourceRconError('Timed out while waiting for reply')
        elif message2:
            raise SourceRconError('Invalid response message: %s' % (repr(message2),))
        return message

    def rcon(self, command):
        """Send RCON command to the server. Connect and auth if necessary,
           handle dropped connections, send command and return reply."""
        if '\n' in command:
            commands = command.split('\n')

            def f(x):
                y = x.strip()
                return len(y) and not y.startswith('//')

            commands = filter(f, commands)
            results = map(self.rcon, commands)
            return ('').join(results)
        try:
            self.send(SERVERDATA_EXECCOMMAND, command)
            return self.receive()
        except:
            self.disconnect()
            self.connect()
            self.send(SERVERDATA_AUTH, self.password)
            auth = self.receive()
            if auth == '':
                auth = self.receive()
            if auth is not True:
                self.disconnect()
                raise SourceRconError('RCON authentication failure: %s' % (repr(auth),))
            self.send(SERVERDATA_EXECCOMMAND, command)
            return self.receive()