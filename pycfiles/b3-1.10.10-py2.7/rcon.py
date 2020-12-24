# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\source\rcon.py
# Compiled at: 2016-03-08 18:42:10
from Queue import Queue
from socket import timeout
from threading import Event
from threading import Lock
from b3.lib.sourcelib.SourceRcon import SourceRcon
from b3.lib.sourcelib.SourceRcon import SourceRconError
from b3.lib.sourcelib.SourceRcon import SERVERDATA_EXECCOMMAND
from b3.lib.sourcelib.SourceRcon import SERVERDATA_AUTH
__version__ = '1.3'
__author__ = 'Courgette'
legacy_receive = SourceRcon.receive

def receive_wrapper(self):
    rv = legacy_receive(self)
    if isinstance(rv, basestring) and rv.strip().endswith(': Bad Password'):
        raise SourceRconError('Bad RCON password (patched SourceRcon)')
    else:
        return rv


SourceRcon.receive = receive_wrapper

class Rcon(object):
    """
    Facade to expose the SourceRcon class with an API as expected by B3 parsers
    """
    lock = Lock()

    def __init__(self, console, host, password):
        """
        Object constructor.
        :param console: The console implementation
        :param host: The host where to send RCON commands
        :param password: The RCON password
        """
        self.console = console
        self.host, self.port = host
        self.password = password
        self.timeout = 1.0
        self.queue = Queue()
        self.stop_event = Event()
        self.server = SourceRcon(self.host, self.port, self.password, self.timeout)
        self.console.info('RCON: connecting to Source game server')
        try:
            self.server.connect()
        except timeout as err:
            self.console.error('RCON: timeout error while trying to connect to game server at %s:%s. Make sure the rcon_ip and port are correct and that the game server is running' % (
             self.host, self.port))

    def writelines(self, lines):
        """
        Sends multiple rcon commands and do not wait for responses (non blocking).
        """
        self.queue.put(lines)

    def write(self, cmd, *args, **kwargs):
        """
        Sends a rcon command and return the response (blocking until timeout).
        """
        with Rcon.lock:
            try:
                self.console.info('RCON SEND: %s' % cmd)
                raw_data = self.server.rcon(self.encode_data(cmd))
                if raw_data:
                    data = raw_data.decode('UTF-8', 'replace')
                    self.console.info('RCON RECEIVED: %s' % data)
                    return data
            except timeout:
                self.console.error('RCON: timeout error while trying to connect to game server at %s:%s. Make sure the rcon_ip and port are correct and that the game server is running' % (
                 self.host, self.port))

    def flush(self):
        pass

    def close(self):
        """
        Disconnects from the source game server.
        """
        if self.server:
            try:
                self.console.info('RCON disconnecting from Source game server')
                self.server.disconnect()
                self.console.verbose('RCON disconnected from Source game server')
            finally:
                self.server = None
                del self.server

        return

    def _writelines(self):
        while not self.stop_event.isSet():
            lines = self.queue.get(True)
            for cmd in lines:
                if not cmd:
                    continue
                with self.lock:
                    self.rconNoWait(cmd)

    def rconNoWait(self, cmd):
        """
        Send a single command, do not wait for any response.
        Connect and auth if necessary.
        """
        try:
            self.console.info('RCON SEND: %s' % cmd)
            self.server.send(SERVERDATA_EXECCOMMAND, self.encode_data(cmd))
        except Exception:
            self.server.disconnect()
            self.server.connect()
            self.server.send(SERVERDATA_AUTH, self.password)
            auth = self.server.receive()
            if auth == '':
                auth = self.server.receive()
            if auth is not True:
                self.server.disconnect()
                raise SourceRconError('RCON authentication failure: %s' % (repr(auth),))
            self.server.send(SERVERDATA_EXECCOMMAND, self.encode_data(cmd))

    def encode_data(self, data):
        """
        Encode data.
        """
        if not data:
            return data
        else:
            if type(data) is unicode:
                return data.encode('UTF-8')
            return data