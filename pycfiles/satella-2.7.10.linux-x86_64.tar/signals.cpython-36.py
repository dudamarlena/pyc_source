# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/posix/signals.py
# Compiled at: 2020-04-14 13:42:23
# Size of source mod 2**32: 1084 bytes
"""
Handle signals, like a boss
"""
import signal, time, typing as tp
end = False

def __sighandler(a, b):
    global end
    end = True


def hang_until_sig(extra_signals: tp.Optional[tp.List[int]]=None, end_on_keyboard_interrupt: bool=True):
    """
    Will hang until this process receives SIGTERM or SIGINT.
    If you pass extra signal IDs (signal.SIG*) with extra_signals,
    then also on those signals this call will release.

    :param extra_signals: a list of extra signals to listen to
    :param end_on_keyboard_interrupt: whether to consider receiving a KeyboardInterrupt as
        a signal to finish
    """
    global end
    extra_signals = extra_signals or []
    signal.signal(signal.SIGTERM, __sighandler)
    signal.signal(signal.SIGINT, __sighandler)
    for s in extra_signals:
        signal.signal(s, __sighandler)

    while not end:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            if end_on_keyboard_interrupt:
                end = True

    end = False