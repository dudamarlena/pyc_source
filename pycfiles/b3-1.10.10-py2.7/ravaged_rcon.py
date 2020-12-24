# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\ravaged\ravaged_rcon.py
# Compiled at: 2016-03-08 18:42:10
import asyncore, logging, re, time
from hashlib import sha1
from socket import AF_INET
from socket import SOCK_STREAM
from threading import Thread
from threading import Event
from threading import Lock
from Queue import Queue
from Queue import Empty
__author__ = 'Thomas LEVEIL'
__version__ = '1.3'

class RavagedServerError(Exception):
    pass


class RavagedServerNetworkError(RavagedServerError):
    pass


class RavagedServerBlacklisted(RavagedServerNetworkError):
    pass


class RavagedServerCommandError(RavagedServerError):
    pass


class RavagedServerCommandTimeout(RavagedServerCommandError):
    pass


class RavagedServer(Thread):
    """
    Thread opening a connection to a Ravaged game server and providing
    means of observing messages received and sending commands
    """

    def __init__(self, host, port=13550, password='', user=None, command_timeout=1.0):
        Thread.__init__(self, name='RavagedServerThread')
        self.password = password
        self.command_timeout = command_timeout
        self.user = user if user else 'Admin'
        self._stopEvent = Event()
        self.__command_reply_event = Event()
        self.__command_lock = Lock()
        self._received_packets = Queue(maxsize=500)
        self.command_response = None
        self.observers = set()
        self.log = logging.getLogger('RavagedServer')
        self.dispatcher = RavagedDispatcher(host, port, self._received_packets)
        self.packet_handler_thread = RavagedServerPacketHandler(self.log, self._received_packets, self._on_event, self._on_command_response)
        self.start()
        time.sleep(0.2)
        return

    def subscribe(self, func):
        """
        Add func from Frosbite events listeners.
        """
        self.observers.add(func)

    def unsubscribe(self, func):
        """
        Remove func from Frosbite events listeners.
        """
        self.observers.remove(func)

    def auth(self):
        self.log.info('authenticating %s' % self.user)
        try:
            response = self.command('LOGIN=%s' % self.user)
            self.log.debug('login response : %r' % response)
            if response.startswith('Suspicious activity detected'):
                raise RavagedServerBlacklisted(response)
        except RavagedServerCommandTimeout:
            pass

        response = self.command('PASS=' + sha1(self.password).hexdigest().upper())
        if response.startswith('Login success as '):
            self.log.info(response)
            try:
                rv = self.command('testrcon')
                if rv != 'Command not found, or invalid parameters given.':
                    raise RavagedServerNetworkError('not properly connected (%s)' % rv)
            except RavagedServerCommandTimeout:
                raise RavagedServerNetworkError('not properly connected')

            return
        if response.startswith('Login failed'):
            self.log.warning(response)
            raise RavagedServerError(response)
        else:
            RavagedServerCommandError('unexpected response: %r' % response)

    def command(self, command):
        """
        Send command to the server in a synchronous way.
        Calling this method will block until we receive the reply packet
        from the game server or until we reach the timeout.
        """
        if not self.connected:
            raise RavagedServerNetworkError('not connected')
        self.log.debug('command : %s ' % repr(command))
        if not command or not len(command.strip()):
            return
        with self.__command_lock:
            self.dispatcher.send_command(command)
            response = self._wait_for_response(command)
            return response
        return

    def stop(self):
        self._stopEvent.set()
        self.dispatcher.close()

    @property
    def connected(self):
        return self.dispatcher.connected

    def getLogger(self):
        return self.log

    def isStopped(self):
        return self._stopEvent.is_set()

    def run(self):
        """
        Threaded code.
        """
        self.packet_handler_thread.start()
        self.log.info('start server loop')
        try:
            try:
                while not self.isStopped():
                    asyncore.loop(count=1, timeout=1)

            except KeyboardInterrupt:
                pass

        finally:
            self.dispatcher.close()

        self.log.info('end server loop')
        self.packet_handler_thread.stop()

    def _on_event(self, message):
        self.log.debug('received server event : %r' % message)
        for func in self.observers:
            func(message)

    def _on_command_response(self, command, response):
        self.log.debug('received server command %r response : %r' % (command, response))
        self.command_response = (command, response)
        self.__command_reply_event.set()

    def _wait_for_response(self, command):
        """
        Block until response to for given command has been received or until timeout is reached.
        """
        l_command = command.lower()
        if l_command.startswith('login='):
            command_name = 'login'
        else:
            if l_command.startswith('pass='):
                command_name = 'pass'
            else:
                command_name = command.split(' ', 1)[0].lower()
            expire_time = time.time() + self.command_timeout
            while not self.isStopped() and self.dispatcher.connected:
                if not self.connected:
                    raise RavagedServerNetworkError('lost connection to server')
                if time.time() >= expire_time:
                    raise RavagedServerCommandTimeout('did not receive any response for %r' % command)
                self.log.debug('waiting for command %r response' % command)
                self.__command_reply_event.clear()
                self.__command_reply_event.wait(self.command_timeout)
                rv = self.command_response
                self.command_response = None
                if rv:
                    cmd, response = rv
                    if cmd and cmd.lower() != command_name:
                        self.log.debug('discarding command response %s:%s' % (cmd, response))
                        continue
                    return response

        return


class RavagedServerPacketHandler(Thread):
    """
    Thread that handles received packets found in received_packets_queue and call the event_handler or
    command_response_handler depending on the nature of the packets.
    """

    def __init__(self, logger, received_packets_queue, event_handler, command_response_handler):
        Thread.__init__(self, name='RavagedServerPacketHandlerThread')
        self.log = logger
        self._stopEvent = Event()
        self._received_packets = received_packets_queue
        self.__event_handler = event_handler
        self.__command_response_handler = command_response_handler
        self.__stop_token = object()

    def run(self):
        """
        Threaded code.
        """
        self.log.info('start server packet handler loop')
        try:
            while not self.isStopped():
                try:
                    packet = self._received_packets.get(timeout=10)
                    if packet is self.__stop_token:
                        break
                    self.handle_packet(packet)
                    self._received_packets.task_done()
                except Empty:
                    pass

        finally:
            pass

        self.log.info('end server packet handler loop')

    def stop(self):
        self._stopEvent.set()
        self._received_packets.put(self.__stop_token)

    def isStopped(self):
        return self._stopEvent.is_set()

    def handle_packet(self, packet):
        """
        Called when a full packet has been received.
        """
        if packet[0] == '(' and packet[(-1)] == ')':
            self.handle_event(packet)
        elif packet.startswith('RCon:('):
            self.handle_event(packet)
        elif packet == 'You must be a superuser to run this command.':
            self.handle_command_response(None, packet)
        else:
            m = re.match(RE_COMMAND_RESPONSE, packet)
            if not m:
                self.handle_event(packet)
            else:
                self.handle_command_response(m.group('command'), m.group('response'))
        return

    def handle_event(self, message):
        if self.__event_handler is not None:
            self.__event_handler(message)
        return

    def handle_command_response(self, command, response):
        if self.__command_response_handler is not None:
            self.__command_response_handler(command, response)
        return


MIN_MESSAGE_LENGTH = 4
RE_COMMAND_RESPONSE = re.compile('^(?P<command>[\\S^:]+):(?P<response>.*)$', re.DOTALL)

class RavagedDispatcher(asyncore.dispatcher_with_send):
    """
    This asyncore dispatcher provides the send_command method to write to the socket
    and exposes a Queue.Queue that stores the received full packets.
    """

    def __init__(self, host, port, packet_queue=None):
        asyncore.dispatcher_with_send.__init__(self)
        self.log = logging.getLogger('RavagedDispatcher')
        self._buffer_in = ''
        self.packet_queue = packet_queue if packet_queue else Queue()
        self.log.info('connecting')
        self.create_socket(AF_INET, SOCK_STREAM)
        self.connect((host, port))

    def send_command(self, command):
        """
        Send a command to the server.
        """
        self.log.debug('send_command : %s ' % repr(command))
        self.send(unicode(command + '\n').encode('UTF-8'))

    def get_packet_queue(self):
        return self.packet_queue

    def handle_connect(self):
        self.log.debug('handle_connect')

    def handle_close(self):
        """
        Called when the socket is closed.
        """
        self.log.debug('handle_close')
        self.close()

    def handle_read(self):
        """
        Called when the asynchronous loop detects that a read() call on the channel's socket will succeed.
        """
        data = self.recv(8192)
        self._buffer_in += data
        self.log.debug('read %s char from server' % len(data))
        map(self.handle_packet, self.full_packets())

    def handle_packet(self, packet):
        """
        Called when a full packet has been received.
        """
        self.log.debug('handle_packet(%r)' % packet)
        self.packet_queue.put(packet)

    def getLogger(self):
        return self.log

    def full_packets(self):
        """
        Generator producing full packets from the data found in self._buffer_in
        :return: packet data (everything but the packet size header)
        """
        while len(self._buffer_in) >= MIN_MESSAGE_LENGTH:
            start_header_index = self._buffer_in.find('(')
            if start_header_index == -1:
                return
            self._buffer_in = self._buffer_in[start_header_index:]
            end_header_index = self._buffer_in.find(')')
            if end_header_index == -1:
                return
            data_size = int(self._buffer_in[1:end_header_index])
            start_data_index = end_header_index + 1
            end_data_index = start_data_index + data_size
            if len(self._buffer_in) < end_data_index:
                return
            packet_data = self._buffer_in[start_data_index:end_data_index]
            self._buffer_in = self._buffer_in[end_data_index:]
            unicode_data = packet_data.decode('UTF-8')
            yield unicode_data