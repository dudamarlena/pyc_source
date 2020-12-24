# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Engine/Poll.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 7222 bytes
__doc__ = '\nA poll() based ClusterShell Engine.\n\nThe poll() system call is available on Linux and BSD.\n'
import errno, logging, select, time
from ClusterShell.Engine.Engine import Engine, E_READ, E_WRITE
from ClusterShell.Engine.Engine import EngineException
from ClusterShell.Engine.Engine import EngineNotSupportedError
from ClusterShell.Engine.Engine import EngineTimeoutException
from ClusterShell.Worker.EngineClient import EngineClientEOF

class EnginePoll(Engine):
    """EnginePoll"""
    identifier = 'poll'

    def __init__(self, info):
        """
        Initialize Engine.
        """
        Engine.__init__(self, info)
        try:
            self.polling = select.poll()
        except AttributeError:
            raise EngineNotSupportedError(EnginePoll.identifier)

    def _register_specific(self, fd, event):
        """Engine-specific fd registering. Called by Engine register."""
        if event & E_READ:
            eventmask = select.POLLIN
        else:
            assert event & E_WRITE
            eventmask = select.POLLOUT
        self.polling.register(fd, eventmask)

    def _unregister_specific(self, fd, ev_is_set):
        if ev_is_set:
            self.polling.unregister(fd)

    def _modify_specific(self, fd, event, setvalue):
        """
        Engine-specific modifications after a interesting event change for
        a file descriptor. Called automatically by Engine register/unregister
        and set_events().  For the poll() engine, it reg/unreg or modifies the
        event mask associated to a file descriptor.
        """
        self._debug('MODSPEC fd=%d event=%x setvalue=%d' % (fd, event,
         setvalue))
        if setvalue:
            self._register_specific(fd, event)
        else:
            self.polling.unregister(fd)

    def runloop(self, timeout):
        """
        Poll engine run(): start clients and properly get replies
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
                    poll_timeo = timeo * 1000.0
                evlist = self.polling.poll(poll_timeo)
            except select.error as ex:
                if ex.args[0] == errno.EINTR:
                    continue
                else:
                    if ex.args[0] == errno.EINVAL:
                        msg = 'Increase RLIMIT_NOFILE?'
                        logging.getLogger(__name__).error(msg)
                raise

            for fd, event in evlist:
                if event & select.POLLNVAL:
                    raise EngineException('Caught POLLNVAL on fd %d' % fd)
                else:
                    client, stream = self._fd2client(fd)
                    if client is None:
                        continue
                    fdev = stream.evmask
                    sname = stream.name
                    self._current_stream = stream
                    if event & select.POLLERR:
                        self._debug('POLLERR %s' % client)
                        assert fdev & E_WRITE
                        self._debug('POLLERR: remove_stream sname %s fdev 0x%x' % (
                         sname, fdev))
                        self.remove_stream(client, stream)
                        self._current_stream = None
                        continue
                    if event & select.POLLIN:
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
                        if event & select.POLLHUP:
                            self._debug('POLLHUP fd=%d %s (%s)' % (
                             fd, client.__class__.__name__, client.streams))
                            self.remove_stream(client, stream)
                            self._current_stream = None
                            continue
                        if event & select.POLLOUT:
                            self._debug('POLLOUT fd=%d %s (%s)' % (
                             fd, client.__class__.__name__, client.streams))
                            assert fdev == E_WRITE
                            assert stream.events & fdev
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