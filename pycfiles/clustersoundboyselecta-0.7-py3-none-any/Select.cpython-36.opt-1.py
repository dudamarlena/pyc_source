# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /ClusterShell/Engine/Select.py
# Compiled at: 2019-12-07 15:34:33
# Size of source mod 2**32: 6522 bytes
__doc__ = '\nA select() based ClusterShell Engine.\n\nThe select() system call is available on almost every UNIX-like systems.\n'
import errno, select, sys, time
from ClusterShell.Engine.Engine import Engine, E_READ, E_WRITE
from ClusterShell.Engine.Engine import EngineTimeoutException
from ClusterShell.Worker.EngineClient import EngineClientEOF

class EngineSelect(Engine):
    """EngineSelect"""
    identifier = 'select'

    def __init__(self, info):
        """
        Initialize Engine.
        """
        Engine.__init__(self, info)
        self._fds_r = []
        self._fds_w = []

    def _register_specific(self, fd, event):
        """
        Engine-specific fd registering. Called by Engine register.
        """
        if event & E_READ:
            self._fds_r.append(fd)
        else:
            assert event & E_WRITE
            self._fds_w.append(fd)

    def _unregister_specific(self, fd, ev_is_set):
        """
        Engine-specific fd unregistering. Called by Engine unregister.
        """
        if ev_is_set or True:
            if fd in self._fds_r:
                self._fds_r.remove(fd)
            if fd in self._fds_w:
                self._fds_w.remove(fd)

    def _modify_specific(self, fd, event, setvalue):
        """
        Engine-specific modifications after a interesting event change
        for a file descriptor. Called automatically by Engine
        register/unregister and set_events(). For the select() engine,
        it appends/remove the fd to/from the concerned fd_sets.
        """
        self._debug('MODSPEC fd=%d event=%x setvalue=%d' % (fd, event,
         setvalue))
        if setvalue:
            self._register_specific(fd, event)
        else:
            self._unregister_specific(fd, True)

    def runloop(self, timeout):
        """
        Select engine run(): start clients and properly get replies
        """
        if not timeout:
            timeout = -1
        start_time = time.time()
        while self.evlooprefcnt > 0:
            self._debug('LOOP evlooprefcnt=%d (reg_clifds=%s) (timers=%d)' % (
             self.evlooprefcnt, self.reg_clifds.keys(), len(self.timerq)))
            try:
                timeo = self.timerq.nextfire_delay()
                if timeout > 0:
                    if timeo >= timeout:
                        self.timerq.clear()
                        timeo = timeout
                if timeo == -1:
                    timeo = timeout
                self._current_loopcnt += 1
                if timeo >= 0:
                    r_ready, w_ready, x_ready = select.select(self._fds_r, self._fds_w, [], timeo)
                else:
                    r_ready, w_ready, x_ready = select.select(self._fds_r, self._fds_w, [])
            except select.error as ex:
                if ex.args[0] == errno.EINTR:
                    continue
                else:
                    if ex.args[0] in (errno.EINVAL, errno.EBADF, errno.ENOMEM):
                        msg = 'Increase RLIMIT_NOFILE?'
                        logging.getLogger(__name__).error(msg)
                raise

            for fd in set(r_ready) | set(w_ready):
                client, stream = self._fd2client(fd)
                if client is None:
                    continue
                fdev = stream.evmask
                sname = stream.name
                self._current_stream = stream
                if fd in r_ready:
                    self._debug('R_READY fd=%d %s (%s)' % (fd,
                     client.__class__.__name__, client.streams))
                    assert fdev & E_READ
                    assert stream.events & fdev
                    self.modify(client, sname, 0, fdev)
                    try:
                        client._handle_read(sname)
                    except EngineClientEOF:
                        self._debug('EngineClientEOF %s' % client)
                        self.remove_stream(client, stream)

                    if fd in w_ready:
                        self._debug('W_READY fd=%d %s (%s)' % (fd,
                         client.__class__.__name__, client.streams))
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