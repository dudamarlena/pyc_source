# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/Kodi/graceful_exit.py
# Compiled at: 2016-01-05 16:02:28
import signal, sys

class Graceful_Exit:

    def __init__(self):
        self.original_sigint = signal.getsignal(signal.SIGINT)

    def __enter__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def __exit__(self, *args):
        signal.signal(signal.SIGINT, self.original_sigint)

    def exit_gracefully(self, signum, frame):
        real_raw_input = vars(__builtins__).get('raw_input', input)
        try:
            if real_raw_input('\nReally quit? (y/n)> ').lower().startswith('y'):
                sys.exit(1)
        except KeyboardInterrupt:
            print 'Ok ok, quitting'
            sys.exit(1)

        signal.signal(signal.SIGINT, self.exit_gracefully)