# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Engine/EPoll.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 7108 bytes
__doc__ = '\nA ClusterShell Engine using epoll, an I/O event notification facility.\n\nThe epoll event distribution interface is available on Linux 2.6, and\nhas been included in Python 2.6.\n'
import errno, select, time
from ClusterShell.Engine.Engine import Engine, E_READ, E_WRITE
from ClusterShell.Engine.Engine import EngineNotSupportedError
from ClusterShell.Engine.Engine import EngineTimeoutException
from ClusterShell.Worker.EngineClient import EngineClientEOF

class EngineEPoll(Engine):
    """EngineEPoll"""
    identifier = 'epoll'

    def __init__(self, info):
        """
        Initialize Engine.
        """
        Engine.__init__(self, info)
        try:
            self.epolling = select.epoll()
        except AttributeError:
            raise EngineNotSupportedError(EngineEPoll.identifier)

    def release(self):
        """Release engine-specific resources."""
        self.epolling.close()

    def _register_specific(self, fd, event):
        """Engine-specific fd registering. Called by Engine register."""
        if event & E_READ:
            eventmask = select.EPOLLIN
        else:
            assert event & E_WRITE
            eventmask = select.EPOLLOUT
        self.epolling.register(fd, eventmask)

    def _unregister_specific(self, fd, ev_is_set):
        """
        Engine-specific fd unregistering. Called by Engine unregister.
        """
        self._debug('UNREGSPEC fd=%d ev_is_set=%x' % (fd, ev_is_set))
        if ev_is_set:
            self.epolling.unregister(fd)

    def _modify_specific(self, fd, event, setvalue):
        """
        Engine-specific modifications after a interesting event change for
        a file descriptor. Called automatically by Engine set_events().
        For the epoll engine, it modifies the event mask associated to a file
        descriptor.
        """
        self._debug('MODSPEC fd=%d event=%x setvalue=%d' % (fd, event,
         setvalue))
        if setvalue:
            self._register_specific(fd, event)
        else:
            self.epolling.unregister(fd)

    def runloop(self, timeout):
        """
        Run epoll main loop.
        """
        if not timeout:
            timeout = -1
        start_time = time.time()
        while self.evlooprefcnt > 0:
            self._debug('LOOP evlooprefcnt=%d (reg_clifds=%s) (timers=%d)' % (
             self.evlooprefcnt, self.reg_clifds.keys(),
             len(self.timerq)))
            try:
                timeo = self.timerq.nextfire_delay()
                if timeout > 0:
                    if timeo >= timeout:
                        self.timerq.clear()
                        timeo = timeout
                if timeo == -1:
                    timeo = timeout
                self._current_loopcnt += 1
                if timeo < 0:
                    poll_timeo = -1
                else:
                    poll_timeo = timeo
                evlist = self.epolling.poll(poll_timeo)
            except IOError as ex:
                if ex.errno == errno.EINTR:
                    continue

            for fd, event in evlist:
                client, stream = self._fd2client(fd)
                if client is None:
                    continue
                fdev = stream.evmask
                sname = stream.name
                self._current_stream = stream
                if event & select.EPOLLERR:
                    self._debug('EPOLLERR fd=%d sname=%s fdev=0x%x (%s)' % (
                     fd, sname, fdev, client))
                    assert fdev & E_WRITE
                    self.remove_stream(client, stream)
                    self._current_stream = None
                else:
                    if event & select.EPOLLIN:
                        if not fdev & E_READ:
                            raise AssertionError
                        else:
                            assert stream.events & fdev, (stream.events, fdev)
                            self.modify(client, sname, 0, fdev)
                            try:
                                client._handle_read(sname)
                            except EngineClientEOF:
                                self._debug('EngineClientEOF %s %s' % (client, sname))
                                self.remove_stream(client, stream)
                                self._current_stream = None
                                continue

                    else:
                        if event & select.EPOLLHUP:
                            assert fdev & E_READ, 'fdev 0x%x & E_READ' % fdev
                            self._debug('EPOLLHUP fd=%d sname=%s %s (%s)' % (
                             fd, sname, client, client.streams))
                            self.remove_stream(client, stream)
                            self._current_stream = None
                            continue
                        if event & select.EPOLLOUT:
                            self._debug('EPOLLOUT fd=%d sname=%s %s (%s)' % (
                             fd, sname, client, client.streams))
                            assert fdev & E_WRITE
                            assert stream.events & fdev, (stream.events, fdev)
                            self.modify(client, sname, 0, fdev)
                            client._handle_write(sname)
                        self._current_stream = None
                        if client.registered:
                            self.set_events(client, stream)

            if timeout > 0:
                if time.time() >= start_time + timeout:
                    raise EngineTimeoutException()
            self.fire_timers()

        self._debug('LOOP EXIT evlooprefcnt=%d (reg_clifds=%s) (timers=%d)' % (
         self.evlooprefcnt, self.reg_clifds, len(self.timerq)))