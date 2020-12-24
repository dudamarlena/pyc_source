# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ClusterShell/Engine/Engine.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 27183 bytes
"""
Interface of underlying Task's Engine.

An Engine implements a loop your thread enters and uses to call event handlers
in response to incoming events (from workers, timers, etc.).
"""
import errno, heapq, logging, sys, time, traceback
LOGGER = logging.getLogger(__name__)
E_READ = 1
E_WRITE = 2
EPSILON = 0.001
FANOUT_UNLIMITED = -1
FANOUT_DEFAULT = None

class EngineException(Exception):
    __doc__ = '\n    Base engine exception.\n    '


class EngineAbortException(EngineException):
    __doc__ = '\n    Raised on user abort.\n    '

    def __init__(self, kill):
        EngineException.__init__(self)
        self.kill = kill


class EngineTimeoutException(EngineException):
    __doc__ = '\n    Raised when a timeout is encountered.\n    '


class EngineIllegalOperationError(EngineException):
    __doc__ = '\n    Error raised when an illegal operation has been performed.\n    '


class EngineAlreadyRunningError(EngineIllegalOperationError):
    __doc__ = '\n    Error raised when the engine is already running.\n    '


class EngineNotSupportedError(EngineException):
    __doc__ = '\n    Error raised when the engine mechanism is not supported.\n    '

    def __init__(self, engineid):
        EngineException.__init__(self)
        self.engineid = engineid


class EngineBaseTimer(object):
    __doc__ = "\n    Abstract class for ClusterShell's engine timer. Such a timer\n    requires a relative fire time (delay) in seconds (as float), and\n    supports an optional repeating interval in seconds (as float too).\n\n    See EngineTimer for more information about ClusterShell timers.\n    "

    def __init__(self, fire_delay, interval=-1.0, autoclose=False):
        """
        Create a base timer.
        """
        if fire_delay is None:
            self.fire_delay = -1.0
        else:
            self.fire_delay = fire_delay
        self.interval = interval
        self.autoclose = autoclose
        self._engine = None
        self._timercase = None

    def _set_engine(self, engine):
        """
        Bind to engine, called by Engine.
        """
        if self._engine:
            raise EngineIllegalOperationError('Already bound to engine.')
        self._engine = engine

    def invalidate(self):
        """
        Invalidates a timer object, stopping it from ever firing again.
        """
        if self._engine:
            self._engine.timerq.invalidate(self)
            self._engine = None

    def is_valid(self):
        """
        Returns a boolean value that indicates whether an EngineTimer
        object is valid and able to fire.
        """
        return self._engine is not None

    def set_nextfire(self, fire_delay, interval=-1):
        """
        Set the next firing delay in seconds for an EngineTimer object.

        The optional parameter `interval' sets the firing interval
        of the timer. If not specified, the timer fires once and then
        is automatically invalidated.

        Time values are expressed in second using floating point
        values. Precision is implementation (and system) dependent.

        It is safe to call this method from the task owning this
        timer object, in any event handlers, anywhere.

        However, resetting a timer's next firing time may be a
        relatively expensive operation. It is more efficient to let
        timers autorepeat or to use this method from the timer's own
        event handler callback (ie. from its ev_timer).
        """
        if not self.is_valid():
            raise EngineIllegalOperationError('Operation on invalid timer.')
        self.fire_delay = fire_delay
        self.interval = interval
        self._engine.timerq.reschedule(self)

    def _fire(self):
        raise NotImplementedError('Derived classes must implement.')


class EngineTimer(EngineBaseTimer):
    __doc__ = "\n    Concrete class EngineTimer\n\n    An EngineTimer object represents a timer bound to an engine that\n    fires at a preset time in the future. Timers can fire either only\n    once or repeatedly at fixed time intervals. Repeating timers can\n    also have their next firing time manually adjusted.\n\n    A timer is not a real-time mechanism; it fires when the task's\n    underlying engine to which the timer has been added is running and\n    able to check if the timer's firing time has passed.\n    "

    def __init__(self, fire_delay, interval, autoclose, handler):
        EngineBaseTimer.__init__(self, fire_delay, interval, autoclose)
        self.eh = handler
        assert self.eh is not None, 'An event handler is needed for timer.'

    def _fire(self):
        self.eh.ev_timer(self)


class _EngineTimerQ(object):

    class _EngineTimerCase(object):
        __doc__ = '\n        Helper class that allows comparisons of fire times, to be easily used\n        in an heapq.\n        '

        def __init__(self, client):
            self.client = client
            self.client._timercase = self
            assert self.client.fire_delay > -EPSILON
            self.fire_date = self.client.fire_delay + time.time()

        def __lt__(self, other):
            return self.fire_date < other.fire_date

        def __cmp__(self, other):
            return cmp(self.fire_date, other.fire_date)

        def arm(self, client):
            assert client is not None
            self.client = client
            self.client._timercase = self
            time_current = time.time()
            if self.client.fire_delay > -EPSILON:
                self.fire_date = self.client.fire_delay + time_current
            else:
                interval = float(self.client.interval)
                assert interval > 0
                self.fire_date += interval
            if self.fire_date < time_current:
                LOGGER.debug('Warning: passed interval time for %r (long running event handler?)', self.client)

        def disarm(self):
            client = self.client
            client._timercase = None
            self.client = None
            return client

        def armed(self):
            return self.client is not None

    def __init__(self, engine):
        """
        Initializer.
        """
        self._engine = engine
        self.timers = []
        self.armed_count = 0

    def __len__(self):
        """
        Return the number of active timers.
        """
        return self.armed_count

    def schedule(self, client):
        """
        Insert and arm a client's timer.
        """
        if client.fire_delay > -EPSILON:
            heapq.heappush(self.timers, _EngineTimerQ._EngineTimerCase(client))
            self.armed_count += 1
            if not client.autoclose:
                self._engine.evlooprefcnt += 1

    def reschedule(self, client):
        """
        Re-insert client's timer.
        """
        if client._timercase:
            self.invalidate(client)
            self._dequeue_disarmed()
            self.schedule(client)

    def invalidate(self, client):
        """
        Invalidate client's timer. Current implementation doesn't really remove
        the timer, but simply flags it as disarmed.
        """
        if not client._timercase:
            client.fire_delay = -1.0
            client.interval = -1.0
            return
        else:
            if self.armed_count <= 0:
                raise ValueError('Engine client timer not found in timer queue')
            client._timercase.disarm()
            self.armed_count -= 1
            client.autoclose or self._engine.evlooprefcnt -= 1

    def _dequeue_disarmed(self):
        """
        Dequeue disarmed timers (sort of garbage collection).
        """
        while len(self.timers) > 0 and not self.timers[0].armed():
            heapq.heappop(self.timers)

    def fire_expired(self):
        """
        Remove expired timers from the queue and fire associated clients.
        """
        self._dequeue_disarmed()
        expired_timercases = []
        now = time.time()
        while self.timers and self.timers[0].fire_date <= now:
            expired_timercases.append(heapq.heappop(self.timers))
            self._dequeue_disarmed()

        for timercase in expired_timercases:
            if not timercase.armed():
                pass
            else:
                client = timercase.disarm()
                client.fire_delay = -1.0
                client._fire()
            if client.fire_delay >= -EPSILON or client.interval > EPSILON:
                timercase.arm(client)
                heapq.heappush(self.timers, timercase)
            else:
                self.armed_count -= 1
                if not client.autoclose:
                    self._engine.evlooprefcnt -= 1

    def nextfire_delay(self):
        """
        Return next timer fire delay (relative time).
        """
        self._dequeue_disarmed()
        if len(self.timers) > 0:
            return max(0.0, self.timers[0].fire_date - time.time())
        else:
            return -1

    def clear(self):
        """
        Stop and clear all timers.
        """
        for timer in self.timers:
            if timer.armed():
                timer.client.invalidate()

        self.timers = []
        self.armed_count = 0


class Engine(object):
    __doc__ = '\n    Base class for ClusterShell Engines.\n\n    Subclasses have to implement a runloop listening for client events.\n    Subclasses that override other than "pure virtual methods" should call\n    corresponding base class methods.\n    '
    identifier = '(none)'

    def __init__(self, info):
        """Initialize base class."""
        self.info = info
        self.info['engine'] = self.identifier
        self._clients = set()
        self._ports = set()
        self._reg_stats = {}
        self.reg_clifds = {}
        self._prev_fanout = 0
        self._current_loopcnt = 0
        self._current_stream = None
        self.timerq = _EngineTimerQ(self)
        self.evlooprefcnt = 0
        self.running = False
        self._exited = False

    def release(self):
        """Release engine-specific resources."""
        pass

    def clients(self):
        """Get a copy of clients set."""
        return self._clients.copy()

    def ports(self):
        """
        Get a copy of ports set.
        """
        return self._ports.copy()

    def _fd2client(self, fd):
        client, stream = self.reg_clifds.get(fd, (None, None))
        if client:
            if client._reg_epoch < self._current_loopcnt:
                return (
                 client, stream)
            LOGGER.debug('_fd2client: ignoring just re-used FD %d', stream.fd)
        return (None, None)

    def _can_register(self, client):
        assert not client.registered
        if not client.delayable or client.worker._fanout == FANOUT_UNLIMITED:
            return True
        else:
            if client.worker._fanout is FANOUT_DEFAULT:
                return self._reg_stats.get('default', 0) < self.info['fanout']
            worker = client.worker
            return self._reg_stats.get(worker, 0) < worker._fanout

    def _update_reg_stats(self, client, offset):
        if client.worker._fanout is FANOUT_DEFAULT:
            key = 'default'
        else:
            key = client.worker
        self._reg_stats.setdefault(key, 0)
        self._reg_stats[key] += offset

    def add(self, client):
        """Add a client to engine."""
        client._set_engine(self)
        if client.delayable:
            self._clients.add(client)
        else:
            self._ports.add(client)
        if self.running:
            if self._can_register(client):
                self.register(client._start())

    def _remove(self, client, abort, did_timeout=False):
        """Remove a client from engine (subroutine)."""
        if client.registered or not client.delayable:
            if client.registered:
                self.unregister(client)
            client._close(abort=abort, timeout=did_timeout)

    def remove(self, client, abort=False, did_timeout=False):
        """
        Remove a client from engine. Does NOT aim to flush individual stream
        read buffers.
        """
        self._debug('REMOVE %s' % client)
        if client.delayable:
            self._clients.remove(client)
        else:
            self._ports.remove(client)
        self._remove(client, abort, did_timeout)
        self.start_clients()

    def remove_stream(self, client, stream):
        """
        Regular way to remove a client stream from engine, performing
        needed read flush as needed. If no more retainable stream
        remains for this client, this method automatically removes the
        entire client from engine.

        This function does nothing if the stream is not registered.
        """
        if stream.fd not in self.reg_clifds:
            LOGGER.debug('remove_stream: %s not registered', stream)
            return
        self.unregister_stream(client, stream)
        client._close_stream(stream.name)
        if client in self._clients:
            if not client.streams.retained():
                self.remove(client)

    def clear(self, did_timeout=False, clear_ports=False):
        """
        Remove all clients. Does not flush read buffers.
        Subclasses that override this method should call base class method.
        """
        all_clients = [
         self._clients]
        if clear_ports:
            all_clients.append(self._ports)
        for clients in all_clients:
            while len(clients) > 0:
                client = clients.pop()
                self._remove(client, True, did_timeout)

    def register(self, client):
        """
        Register an engine client. Subclasses that override this method
        should call base class method.
        """
        if not client in self._clients:
            if not client in self._ports:
                raise AssertionError
        else:
            assert not client.registered
            self._debug('REG %s (%s)(autoclose=%s)' % (
             client.__class__.__name__, client.streams,
             client.autoclose))
            client.registered = True
            client._reg_epoch = self._current_loopcnt
            if client.delayable:
                self._update_reg_stats(client, 1)
        for streams, ievent in ((client.streams.active_readers, E_READ),
         (
          client.streams.active_writers, E_WRITE)):
            for stream in streams():
                self.reg_clifds[stream.fd] = (
                 client, stream)
                stream.events |= ievent
                if not client.autoclose:
                    self.evlooprefcnt += 1
                self._register_specific(stream.fd, ievent)

        self.timerq.schedule(client)

    def unregister_stream(self, client, stream):
        """Unregister a stream from a client."""
        self._debug('UNREG_STREAM stream=%s' % stream)
        if not (stream is not None and stream.fd is not None):
            raise AssertionError
        else:
            assert stream.fd in self.reg_clifds, 'stream fd %d not registered' % stream.fd
            assert client.registered
        self._unregister_specific(stream.fd, stream.events & stream.evmask)
        self._debug('UNREG_STREAM unregistering stream fd %d (%d)' % (
         stream.fd, len(client.streams)))
        stream.events &= ~stream.evmask
        del self.reg_clifds[stream.fd]
        if not client.autoclose:
            self.evlooprefcnt -= 1

    def unregister(self, client):
        """Unregister a client"""
        assert client.registered
        self._debug('UNREG %s (%s)' % (client.__class__.__name__,
         client.streams))
        self.timerq.invalidate(client)
        for streams, ievent in ((client.streams.active_readers, E_READ),
         (
          client.streams.active_writers, E_WRITE)):
            for stream in streams():
                if stream.fd in self.reg_clifds:
                    self._unregister_specific(stream.fd, stream.events & ievent)
                    stream.events &= ~ievent
                    del self.reg_clifds[stream.fd]
                    if not client.autoclose:
                        self.evlooprefcnt -= 1

        client.registered = False
        if client.delayable:
            self._update_reg_stats(client, -1)

    def modify(self, client, sname, setmask, clearmask):
        """Modify the next loop interest events bitset for a client stream."""
        self._debug('MODEV set:0x%x clear:0x%x %s (%s)' % (setmask, clearmask,
         client, sname))
        stream = client.streams[sname]
        stream.new_events &= ~clearmask
        stream.new_events |= setmask
        if self._current_stream is not stream:
            self.set_events(client, stream)

    def _register_specific(self, fd, event):
        """Engine-specific register fd for event method."""
        raise NotImplementedError('Derived classes must implement.')

    def _unregister_specific(self, fd, ev_is_set):
        """Engine-specific unregister fd method."""
        raise NotImplementedError('Derived classes must implement.')

    def _modify_specific(self, fd, event, setvalue):
        """Engine-specific modify fd for event method."""
        raise NotImplementedError('Derived classes must implement.')

    def set_events(self, client, stream):
        """Set the active interest events bitset for a client stream."""
        self._debug('SETEV new_events:0x%x events:0x%x for %s[%s]' % (
         stream.new_events, stream.events, client, stream.name))
        if not client.registered:
            LOGGER.debug('set_events: client %s not registered', self)
            return
        chgbits = stream.new_events ^ stream.events
        if chgbits == 0:
            return
        for interest in (E_READ, E_WRITE):
            if chgbits & interest:
                assert stream.evmask & interest
                status = stream.new_events & interest
                self._modify_specific(stream.fd, interest, status)
                if status:
                    stream.events |= interest
                else:
                    stream.events &= ~interest

        stream.new_events = stream.events

    def set_reading(self, client, sname):
        """Set client reading state."""
        self.modify(client, sname, E_READ, 0)

    def set_writing(self, client, sname):
        """Set client writing state."""
        self.modify(client, sname, E_WRITE, 0)

    def add_timer(self, timer):
        """Add a timer instance to engine."""
        timer._set_engine(self)
        self.timerq.schedule(timer)

    def remove_timer(self, timer):
        """Remove engine timer from engine."""
        self.timerq.invalidate(timer)

    def fire_timers(self):
        """Fire expired timers for processing."""
        if self.evlooprefcnt > 0:
            self.timerq.fire_expired()

    def start_ports(self):
        """Start and register all port clients."""
        for port in self._ports:
            if not port.registered:
                self._debug('START PORT %s' % port)
                self.register(port)

    def start_clients(self):
        """Start and register regular engine clients in respect of fanout."""
        fanout_diff = self.info['fanout'] - self._prev_fanout
        if fanout_diff:
            self._prev_fanout = self.info['fanout']
        for client in self._clients:
            if not client.registered:
                if self._can_register(client):
                    self._debug('START CLIENT %s' % client.__class__.__name__)
                    self.register(client._start())
                    if fanout_diff == 0:
                        break

    def run(self, timeout):
        """Run engine in calling thread."""
        if self.running:
            raise EngineAlreadyRunningError()
        try:
            try:
                self.running = True
                self.start_ports()
                self.snoop_ports()
                self.start_clients()
                self.runloop(timeout)
            except EngineTimeoutException:
                self.clear(did_timeout=True)
                raise
            except:
                exc_t, exc_val, exc_tb = sys.exc_info()
                try:
                    self.clear()
                except:
                    tbexc = traceback.format_exception(exc_t, exc_val, exc_tb)
                    LOGGER.debug(''.join(tbexc))
                    raise

                raise

        finally:
            self.timerq.clear()
            self.running = False
            self._prev_fanout = 0

    def snoop_ports(self):
        """
        Peek in ports for possible early pending messages.
        This method simply tries to read port pipes in non-blocking mode.
        """
        ports = self._ports.copy()
        for port in ports:
            try:
                port._handle_read('in')
            except (IOError, OSError) as ex:
                if ex.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                    return
                raise

    def runloop(self, timeout):
        """Engine specific run loop. Derived classes must implement."""
        raise NotImplementedError('Derived classes must implement.')

    def abort(self, kill):
        """Abort runloop."""
        if self.running:
            raise EngineAbortException(kill)
        self.clear(clear_ports=kill)

    def exited(self):
        """Returns True if the engine has exited the runloop once."""
        return not self.running and self._exited

    def _debug(self, s):
        """library engine verbose debugging hook"""
        pass