# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/afx/startup.py
# Compiled at: 2007-11-19 02:07:21
from __future__ import absolute_import, division, generators, with_statement
from functools import partial
from contextlib import contextmanager
import signal
from commons import log, startup
import af
from .threads import call_from_thread, start_thread_pool, stop_thread_pool, waker, watcher
from .pubsub import is_task
__all__ = [
 'reg_signal', 'run_main']

def reg_signal(signum, handler):
    signal.signal(signum, partial(call_from_thread, handler))


@af.task
def exiter(do_kintr):
    q = af.channel(1)

    @af.task
    def do_exit(*args):
        log.debug('afx', 'got keyboard interrupt, exiting')
        yield q.put(0)

    if not do_kintr:
        reg_signal(signal.SIGINT, do_exit)
    reg_signal(signal.SIGTERM, do_exit)
    yield q.get()


def run_main(main=None, do_force=False, use_threads=True, use_exiter=True, do_kintr=False, use_sigquit_handler=False):

    def runner(main, argv):
        tasks = [
         main(argv)]
        if use_threads:
            start_thread_pool()
            tasks.extend([watcher(), waker()])
            if use_exiter:
                tasks.append(exiter(do_kintr))

        @af.task
        def main_task():
            yield af.any(tasks)

        try:
            try:
                reactor = af.event_loop(main_task)
                (exc, res) = reactor.main(True)
            except KeyboardInterrupt:
                (exc, res) = (None, None)

        finally:
            if use_threads:
                stop_thread_pool()

        if exc:
            (ty, v, tr) = exc
            raise ty, v, tr
        log.debug(__name__, 'runner end')
        return

    startup.run_main(main, do_force, runner, use_sigquit_handler)