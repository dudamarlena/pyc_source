# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nls/.virtualenvs/pysher/lib/python3.6/site-packages/pysher/connection.py
# Compiled at: 2020-03-30 13:48:15
# Size of source mod 2**32: 11183 bytes
import sched
from threading import Thread
from collections import defaultdict
import websocket, logging, time, json

class Connection(Thread):

    def __init__(self, event_handler, url, reconnect_handler=None, log_level=None, daemon=True, reconnect_interval=10, socket_kwargs=None, **thread_kwargs):
        self.event_handler = event_handler
        self.url = url
        self.reconnect_handler = reconnect_handler or (lambda : None)
        self.socket = None
        self.socket_id = ''
        self.event_callbacks = defaultdict(list)
        self.disconnect_called = False
        self.needs_reconnect = False
        self.default_reconnect_interval = reconnect_interval
        self.reconnect_interval = reconnect_interval
        self.socket_kwargs = socket_kwargs or dict()
        self.pong_timer = None
        self.pong_received = False
        self.pong_timeout = 30
        self.bind('pusher:connection_established', self._connect_handler)
        self.bind('pusher:connection_failed', self._failed_handler)
        self.bind('pusher:pong', self._pong_handler)
        self.bind('pusher:ping', self._ping_handler)
        self.bind('pusher:error', self._pusher_error_handler)
        self.state = 'initialized'
        self.logger = logging.getLogger(self.__module__)
        if log_level:
            self.logger.setLevel(log_level)
            if log_level == logging.DEBUG:
                websocket.enableTrace(True)
        self.connection_timeout = 305
        self.connection_timer = None
        self.ping_interval = 120
        self.ping_timer = None
        self.timeout_scheduler = sched.scheduler(time.time, sleep_max_n(min([self.pong_timeout, self.connection_timeout, self.ping_interval])))
        self.timeout_scheduler_thread = None
        (Thread.__init__)(self, **thread_kwargs)
        self.daemon = daemon
        self.name = 'PysherEventLoop'

    def bind(self, event_name, callback, *args, **kwargs):
        """Bind an event to a callback

        :param event_name: The name of the event to bind to.
        :type event_name: str

        :param callback: The callback to notify of this event.
        """
        self.event_callbacks[event_name].append((callback, args, kwargs))

    def disconnect(self, timeout=None):
        self.needs_reconnect = False
        self.disconnect_called = True
        if self.socket:
            self.socket.close()
        self.join(timeout)

    def reconnect(self, reconnect_interval=None):
        if reconnect_interval is None:
            reconnect_interval = self.default_reconnect_interval
        self.logger.info('Connection: Reconnect in %s' % reconnect_interval)
        self.reconnect_interval = reconnect_interval
        self.needs_reconnect = True
        if self.socket:
            self.socket.close()

    def run(self):
        self._connect()

    def _connect(self):
        self.state = 'connecting'
        self.socket = websocket.WebSocketApp((self.url),
          on_open=(self._on_open),
          on_message=(self._on_message),
          on_error=(self._on_error),
          on_close=(self._on_close))
        (self.socket.run_forever)(**self.socket_kwargs)
        while self.needs_reconnect and not self.disconnect_called:
            self.logger.info('Attempting to connect again in %s seconds.' % self.reconnect_interval)
            self.state = 'unavailable'
            time.sleep(self.reconnect_interval)
            self.socket.keep_running = True
            (self.socket.run_forever)(**self.socket_kwargs)

    def _on_open(self):
        self.logger.info('Connection: Connection opened')
        self.send_ping()
        self._start_timers()

    def _on_error(self, error):
        self.logger.info('Connection: Error - %s' % error)
        self.state = 'failed'
        self.needs_reconnect = True

    def _on_message(self, message):
        self.logger.info('Connection: Message - %s' % message)
        self._stop_timers()
        params = self._parse(message)
        if 'event' in params.keys():
            if 'channel' not in params.keys():
                if params['event'] in self.event_callbacks.keys():
                    for func, args, kwargs in self.event_callbacks[params['event']]:
                        try:
                            func(params.get('data', None), *args, **kwargs)
                        except Exception:
                            self.logger.exception('Callback raised unhandled')

                else:
                    self.logger.info('Connection: Unhandled event')
            else:
                self.event_handler(params['event'], params['data'], params['channel'])
        self._start_timers()

    def _on_close(self, *args):
        self.logger.info('Connection: Connection closed')
        self.state = 'disconnected'
        self._stop_timers()

    @staticmethod
    def _parse(message):
        return json.loads(message)

    def _stop_timers(self):
        for event in self.timeout_scheduler.queue:
            self._cancel_scheduler_event(event)

    def _start_timers(self):
        self._stop_timers()
        self.ping_timer = self.timeout_scheduler.enter(self.ping_interval, 1, self.send_ping)
        self.connection_timer = self.timeout_scheduler.enter(self.connection_timeout, 2, self._connection_timed_out)
        if not self.timeout_scheduler_thread:
            self.timeout_scheduler_thread = Thread(target=(self.timeout_scheduler.run), daemon=True, name='PysherScheduler')
            self.timeout_scheduler_thread.start()
        elif not self.timeout_scheduler_thread.is_alive():
            self.timeout_scheduler_thread = Thread(target=(self.timeout_scheduler.run), daemon=True, name='PysherScheduler')
            self.timeout_scheduler_thread.start()

    def _cancel_scheduler_event(self, event):
        try:
            self.timeout_scheduler.cancel(event)
        except ValueError:
            self.logger.info('Connection: Scheduling event already cancelled')

    def send_event(self, event_name, data, channel_name=None):
        """Send an event to the Pusher server.

        :param str event_name:
        :param Any data:
        :param str channel_name:
        """
        event = {'event':event_name, 
         'data':data}
        if channel_name:
            event['channel'] = channel_name
        self.logger.info('Connection: Sending event - %s' % event)
        try:
            self.socket.send(json.dumps(event))
        except Exception as e:
            self.logger.error('Failed send event: %s' % e)

    def send_ping(self):
        self.logger.info('Connection: ping to pusher')
        try:
            self.socket.send(json.dumps({'event':'pusher:ping',  'data':''}))
        except Exception as e:
            self.logger.error('Failed send ping: %s' % e)

        self.pong_timer = self.timeout_scheduler.enter(self.pong_timeout, 3, self._check_pong)

    def send_pong(self):
        self.logger.info('Connection: pong to pusher')
        try:
            self.socket.send(json.dumps({'event':'pusher:pong',  'data':''}))
        except Exception as e:
            self.logger.error('Failed send pong: %s' % e)

    def _check_pong(self):
        self._cancel_scheduler_event(self.pong_timer)
        if self.pong_received:
            self.pong_received = False
        else:
            self.logger.info('Did not receive pong in time.  Will attempt to reconnect.')
            self.state = 'failed'
            self.reconnect()

    def _connect_handler(self, data):
        parsed = json.loads(data)
        self.socket_id = parsed['socket_id']
        self.state = 'connected'
        if self.needs_reconnect:
            self.needs_reconnect = False
            self.reconnect_handler()
            self.logger.debug('Connection: Establisheds reconnection')
        else:
            self.logger.debug('Connection: Establisheds first connection')

    def _failed_handler(self, data):
        self.state = 'failed'

    def _ping_handler(self, data):
        self.send_pong()
        self._start_timers()

    def _pong_handler(self, data):
        self.logger.info('Connection: pong from pusher')
        self.pong_received = True

    def _pusher_error_handler--- This code section failed: ---

 L. 278         0  LOAD_STR                 'code'
                2  LOAD_FAST                'data'
                4  COMPARE_OP               in
                6  POP_JUMP_IF_FALSE   174  'to 174'

 L. 280         8  SETUP_EXCEPT         26  'to 26'

 L. 281        10  LOAD_GLOBAL              int
               12  LOAD_FAST                'data'
               14  LOAD_STR                 'code'
               16  BINARY_SUBSCR    
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'error_code'
               22  POP_BLOCK        
               24  JUMP_FORWARD         42  'to 42'
             26_0  COME_FROM_EXCEPT      8  '8'

 L. 282        26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 283        32  LOAD_CONST               None
               34  STORE_FAST               'error_code'
               36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'
             42_1  COME_FROM            24  '24'

 L. 285        42  LOAD_FAST                'error_code'
               44  LOAD_CONST               None
               46  COMPARE_OP               is-not
               48  POP_JUMP_IF_FALSE   160  'to 160'

 L. 286        50  LOAD_FAST                'self'
               52  LOAD_ATTR                logger
               54  LOAD_ATTR                error
               56  LOAD_STR                 'Connection: Received error %s'
               58  LOAD_FAST                'error_code'
               60  BINARY_MODULO    
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  POP_TOP          

 L. 288        66  LOAD_FAST                'error_code'
               68  LOAD_CONST               4000
               70  COMPARE_OP               >=
               72  POP_JUMP_IF_FALSE   104  'to 104'
               74  LOAD_FAST                'error_code'
               76  LOAD_CONST               4099
               78  COMPARE_OP               <=
               80  POP_JUMP_IF_FALSE   104  'to 104'

 L. 290        82  LOAD_FAST                'self'
               84  LOAD_ATTR                logger
               86  LOAD_ATTR                info
               88  LOAD_STR                 'Connection: Error is unrecoverable.  Disconnecting'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  POP_TOP          

 L. 291        94  LOAD_FAST                'self'
               96  LOAD_ATTR                disconnect
               98  CALL_FUNCTION_0       0  '0 positional arguments'
              100  POP_TOP          
              102  JUMP_ABSOLUTE       172  'to 172'
            104_0  COME_FROM            72  '72'

 L. 292       104  LOAD_FAST                'error_code'
              106  LOAD_CONST               4100
              108  COMPARE_OP               >=
              110  POP_JUMP_IF_FALSE   130  'to 130'
              112  LOAD_FAST                'error_code'
              114  LOAD_CONST               4199
              116  COMPARE_OP               <=
              118  POP_JUMP_IF_FALSE   130  'to 130'

 L. 294       120  LOAD_FAST                'self'
              122  LOAD_ATTR                reconnect
              124  CALL_FUNCTION_0       0  '0 positional arguments'
              126  POP_TOP          
              128  JUMP_ABSOLUTE       172  'to 172'
            130_0  COME_FROM           110  '110'

 L. 295       130  LOAD_FAST                'error_code'
              132  LOAD_CONST               4200
              134  COMPARE_OP               >=
              136  POP_JUMP_IF_FALSE   172  'to 172'
              138  LOAD_FAST                'error_code'
              140  LOAD_CONST               4299
              142  COMPARE_OP               <=
              144  POP_JUMP_IF_FALSE   172  'to 172'

 L. 297       146  LOAD_FAST                'self'
              148  LOAD_ATTR                reconnect
              150  LOAD_CONST               0
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  POP_TOP          
              156  JUMP_ABSOLUTE       172  'to 172'

 L. 299       158  JUMP_ABSOLUTE       186  'to 186'
              160  ELSE                     '172'

 L. 301       160  LOAD_FAST                'self'
              162  LOAD_ATTR                logger
              164  LOAD_ATTR                error
              166  LOAD_STR                 'Connection: Unknown error code'
              168  CALL_FUNCTION_1       1  '1 positional argument'
              170  POP_TOP          
            172_0  COME_FROM           144  '144'
              172  JUMP_FORWARD        186  'to 186'
              174  ELSE                     '186'

 L. 303       174  LOAD_FAST                'self'
              176  LOAD_ATTR                logger
              178  LOAD_ATTR                error
              180  LOAD_STR                 'Connection: No error code supplied'
              182  CALL_FUNCTION_1       1  '1 positional argument'
              184  POP_TOP          
            186_0  COME_FROM           172  '172'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 158

    def _connection_timed_out(self):
        self.logger.info('Did not receive any data in time.  Reconnecting.')
        self.state = 'failed'
        self.reconnect()


def sleep_max_n(max_sleep_time):

    def sleep(time_to_sleep):
        time.sleep(min(max_sleep_time, time_to_sleep))

    return sleep