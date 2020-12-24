# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\frostbite\connection.py
# Compiled at: 2016-03-08 18:42:09
__author__ = 'Courgette'
__version__ = '2.1'
debug = True
import socket, string, b3.parsers.frostbite.protocol as protocol

class FrostbiteException(Exception):
    pass


class FrostbiteNetworkException(FrostbiteException):
    pass


class FrostbiteBadPasswordException(FrostbiteException):
    pass


class FrostbiteCommandFailedError(Exception):
    pass


class FrostbiteConnection(object):
    console = None
    _serverSocket = None
    _receiveBuffer = None
    _host = None
    _port = None
    _password = None

    def __init__(self, console, host, port, password):
        """
        Object constructor.
        :param console: The console implementation
        :param host: The host where to connect
        :param port: The port to use for the connection
        :param password: The password for authentication
        """
        self.console = console
        self._host = host
        self._port = port
        self._password = password
        try:
            self._connect()
            self._auth()
        except socket.error as detail:
            raise FrostbiteNetworkException('cannot create FrostbiteConnection: %s' % detail)

    def __del__(self):
        self.close()

    def _connect(self):
        """
        Establish the connection with the Frostbite server.
        """
        try:
            self.console.debug('opening FrostbiteConnection socket')
            self._receiveBuffer = ''
            self._serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._serverSocket.connect((self._host, self._port))
        except Exception as err:
            raise FrostbiteException(err)

    def close(self):
        """
        Close the connection with the Frostbite server.
        """
        if self._serverSocket is not None:
            self.console.debug('closing FrostbiteConnection socket')
            try:
                self.sendRequest('quit')
            except:
                pass

            self._serverSocket.close()
            self._serverSocket = None
        return

    def sendRequest(self, *command):
        """
        Send a request to the Frostbite server.
        """
        if command is None:
            return
        else:
            if self._serverSocket is None:
                self.console.info('sendRequest: reconnecting...')
                self._connect()
                self._auth()
            if len(command) == 1 and type(command[0]) == tuple:
                words = command[0]
            else:
                words = command
            request = protocol.EncodeClientRequest(words)
            self.printPacket(protocol.DecodePacket(request))
            try:
                self._serverSocket.sendall(request)
                response, self._receiveBuffer = protocol.receivePacket(self._serverSocket, self._receiveBuffer)
            except socket.error as detail:
                raise FrostbiteNetworkException(detail)

            if response is None:
                return
            decodedResponse = protocol.DecodePacket(response)
            self.printPacket(decodedResponse)
            return decodedResponse[3]

    def _auth(self):
        """
        Authorize against the Frostbite server.
        """
        self.console.debug('authing to Frostbite server')
        if self._serverSocket is None:
            raise FrostbiteNetworkException('cannot auth, need to be connected')
        words = self.sendRequest('login.hashed')
        if words[0] != 'OK':
            raise FrostbiteException('Could not retrieve salt')
        salt = words[1].decode('hex')
        passwordHash = protocol.generatePasswordHash(salt, self._password)
        passwordHashHexString = string.upper(passwordHash.encode('hex'))
        loginResponse = self.sendRequest('login.hashed', passwordHashHexString)
        if loginResponse[0] != 'OK':
            raise FrostbiteBadPasswordException('The Frostbite server refused our password')
        return

    def subscribeToEvents(self):
        """
        Tell the frostbite server to send us events.
        """
        self.console.debug('subscribing to Frostbite events')
        response = self.sendRequest('eventsEnabled', 'true')
        if response[0] != 'OK':
            raise FrostbiteCommandFailedError(response)

    def readEvent(self):
        """
        Wait event from the server.
        """
        packet = None
        timeout_counter = 0
        while packet is None:
            try:
                if self._serverSocket is None:
                    self.console.info('readEvent: reconnecting...')
                    self._connect()
                    self._auth()
                    self.subscribeToEvents()
                tmppacket, self._receiveBuffer = protocol.receivePacket(self._serverSocket, self._receiveBuffer)
                isFromServer, isResponse, sequence, words = protocol.DecodePacket(tmppacket)
                if isFromServer and not isResponse:
                    packet = tmppacket
                else:
                    self.console.verbose2('received a packet which is not an event: %s' % [isFromServer, isResponse,
                     sequence, words])
            except socket.timeout:
                timeout_counter += 1
                self.console.verbose2('timeout %s' % timeout_counter)
                if timeout_counter >= 5:
                    self.console.verbose2('checking connection...')
                    request = protocol.EncodeClientRequest(['eventsEnabled', 'true'])
                    self.printPacket(protocol.DecodePacket(request))
                    self._serverSocket.sendall(request)
                    timeout_counter = 0
            except socket.error as detail:
                raise FrostbiteNetworkException('readEvent: %r' % detail)

        try:
            isFromServer, isResponse, sequence, words = protocol.DecodePacket(packet)
            self.printPacket(protocol.DecodePacket(packet))
        except:
            raise FrostbiteException('readEvent: failed to decodePacket {%s}' % packet)

        if isResponse:
            self.console.debug('received an unexpected response packet from server, ignoring: %r' % packet)
            return self.readEvent()
        else:
            response = protocol.EncodePacket(True, True, sequence, ['OK'])
            self.printPacket(protocol.DecodePacket(response))
            try:
                self._serverSocket.sendall(response)
            except socket.error as detail:
                self.console.warning('in readEvent while sending response OK to server : %s' % detail)

            return words
            return

    def printPacket(self, packet):
        """
        Display contents of packet in user-friendly format, useful for debugging purposes.
        """
        if debug:
            isFromServer = packet[0]
            isResponse = packet[1]
            msg = ''
            if isFromServer and isResponse:
                msg += '<-R-'
            elif isFromServer and not isResponse:
                msg += '-Q->'
            elif not isFromServer and isResponse:
                msg += '-R->'
            elif not isFromServer and not isResponse:
                msg += '<-Q-'
            msg += ' (%s)' % packet[2]
            if packet[3]:
                msg += ' :'
                for word in packet[3]:
                    msg += ' "' + word + '"'

            self.console.verbose2(msg)