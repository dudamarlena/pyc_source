# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: att/Network/RawServer.py
# Compiled at: 2017-03-18 13:14:54
import sys, bisect, socket, select, threading
from cStringIO import StringIO
from traceback import print_exc
from .SocketHandler import SocketHandler
from att.clock import clock

def autodetect_ipv6():
    try:
        assert socket.has_ipv6
        socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    except (AssertionError, socket.error):
        return 0

    return 1


def autodetect_socket_style():
    if sys.platform.find('linux') < 0:
        return 1
    try:
        with open('/proc/sys/net/ipv6/bindv6only', 'r') as (f):
            dual_socket_style = int(f.read())
        return int(not dual_socket_style)
    except (IOError, ValueError):
        return 0


READSIZE = 32768

class RawServer(object):

    def __init__(self, doneflag, timeout_check_interval, timeout, noisy=True, ipv6_enable=True, failfunc=lambda x: None, errorfunc=None, sockethandler=None, excflag=threading.Event()):
        self.timeout_check_interval = max(timeout_check_interval, 0)
        self.timeout = timeout
        self.servers = {}
        self.single_sockets = {}
        self.dead_from_write = []
        self.doneflag = doneflag
        self.noisy = noisy
        self.failfunc = failfunc
        self.errorfunc = errorfunc
        self.exccount = 0
        self.funcs = []
        self.externally_added = []
        self.finished = threading.Event()
        self.tasks_to_kill = set()
        self.excflag = excflag
        if sockethandler is None:
            sockethandler = SocketHandler(timeout, ipv6_enable, READSIZE)
        self.sockethandler = sockethandler
        self.find_and_bind = sockethandler.find_and_bind
        self.start_connection = sockethandler.start_connection
        self.get_stats = sockethandler.get_stats
        self.bind = sockethandler.bind
        self.start_connection_raw = sockethandler.start_connection_raw
        self.add_task(self.scan_for_timeouts, timeout_check_interval)
        return

    def get_exception_flag(self):
        return self.excflag

    def add_task(self, func, delay=0, tid=None):
        assert float(delay) >= 0
        self.externally_added.append((func, delay, tid))

    def pop_external(self):
        """Prepare tasks queued with add_task to be run in the listen_forever
        loop."""
        to_add, self.externally_added = self.externally_added, []
        for func, delay, tid in to_add:
            if tid not in self.tasks_to_kill:
                bisect.insort(self.funcs, (clock() + delay, func, tid))

    def scan_for_timeouts(self):
        self.add_task(self.scan_for_timeouts, self.timeout_check_interval)
        self.sockethandler.scan_for_timeouts()

    def listen_forever(self, handler):
        self.sockethandler.set_handler(handler)
        try:
            while not self.doneflag.isSet():
                try:
                    self.pop_external()
                    self._kill_tasks()
                    if self.funcs:
                        period = max(0, self.funcs[0][0] + 0.001 - clock())
                    else:
                        period = 1073741824
                    events = self.sockethandler.do_poll(period)
                    if self.doneflag.isSet():
                        return
                    while self.funcs and self.funcs[0][0] <= clock():
                        _, func, tid = self.funcs.pop(0)
                        if tid in self.tasks_to_kill:
                            pass
                        try:
                            func()
                        except (SystemError, MemoryError) as e:
                            self.failfunc(str(e))
                            return
                        except KeyboardInterrupt:
                            return
                        except Exception:
                            if self.noisy:
                                self.exception()

                    self.sockethandler.close_dead()
                    self.sockethandler.handle_events(events)
                    if self.doneflag.isSet():
                        return
                    self.sockethandler.close_dead()
                except (SystemError, MemoryError) as e:
                    self.failfunc(str(e))
                    return
                except select.error:
                    if self.doneflag.isSet():
                        return
                except KeyboardInterrupt:
                    return
                except Exception:
                    self.exception()

                if self.exccount > 10:
                    return

        finally:
            self.finished.set()

    def is_finished(self):
        return self.finished.isSet()

    def wait_until_finished(self):
        self.finished.wait()

    def _kill_tasks(self):
        if self.tasks_to_kill:
            self.funcs = [ (t, func, tid) for t, func, tid in self.funcs if tid not in self.tasks_to_kill ]
            self.tasks_to_kill = set()

    def kill_tasks(self, tid):
        self.tasks_to_kill.add(tid)

    def exception(self, kbint=False):
        if not kbint:
            self.excflag.set()
        self.exccount += 1
        if self.errorfunc is None:
            print_exc()
        else:
            data = StringIO()
            print_exc(file=data)
            if not kbint:
                self.errorfunc(data.getvalue())
        return

    def shutdown(self):
        self.sockethandler.shutdown()