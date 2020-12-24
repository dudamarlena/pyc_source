# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/Kodi/defer_signals.py
# Compiled at: 2016-01-05 16:04:08
import os, signal

class defer_signals(object):
    """
    Context manager to defer signal handling until context exits.

    Takes optional list of signals to defer (default: SIGHUP, SIGINT, SIGTERM).
    Signals can be identified by number or by name.

    Allows you to wrap instruction sequences that ought to be atomic and ensure
    that they don't get interrupted mid-way.
    """

    def __init__(self, signal_list=None):
        if signal_list is None:
            signal_list = [
             signal.SIGHUP, signal.SIGINT, signal.SIGTERM]
        self.signal_list = [ getattr(signal, sig_id) if isinstance(sig_id, basestring) else sig_id for sig_id in signal_list
                           ]
        self.deferred = []
        self.previous_handlers = {}
        return

    def defer_signal(self, sig_num, stack_frame):
        self.deferred.append(sig_num)

    def __enter__(self):
        for sig_num in self.signal_list:
            self.previous_handlers[sig_num] = signal.signal(sig_num, self.defer_signal) or signal.SIG_DFL

        return self

    def __exit__(self, *args):
        for sig_num, handler in self.previous_handlers.items():
            signal.signal(sig_num, handler)

        while self.deferred:
            sig_num = self.deferred.pop(0)
            os.kill(os.getpid(), sig_num)

    def __call__(self):
        """
        If there are any deferred signals pending, trigger them now

        This means that instead of this code:

            for item in collection:
                with defer_signals():
                    item.process()

        You can write this:

            with defer_signals() as handle_signals:
                for item in collection:
                    item.process()
                    handle_signals()

        Which has the same effect but avoids having to embed the context
        manager in the loop
        """
        if self.deferred:
            self.__exit__()
            self.__enter__()