# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/devenv/common/timeout.py
# Compiled at: 2016-03-01 07:13:25
import signal

class timeout:

    def __init__(self, seconds=1):
        self.seconds = seconds

    def handle_timeout(self, signum, frame):
        raise Exception('Timeout')

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)