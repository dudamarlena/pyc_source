# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/etheno/signals.py
# Compiled at: 2019-06-27 23:49:12
# Size of source mod 2**32: 478 bytes
import signal

def add_handler(signal_type, handler):
    current_handler = signal.getsignal(signal_type)
    if current_handler == signal.SIG_IGN or current_handler == signal.SIG_DFL:
        current_handler = None

    def new_handler(sig_type, frame):
        if current_handler:
            current_handler(sig_type, frame)
        handler(sig_type, frame)

    signal.signal(signal_type, new_handler)


def add_sigint_handler(handler):
    add_handler(signal.SIGINT, handler)