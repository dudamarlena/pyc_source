# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/litebo/utils/limit.py
# Compiled at: 2020-05-03 05:18:21
# Size of source mod 2**32: 915 bytes
import sys
from contextlib import contextmanager
if sys.platform != 'win32':
    import signal

def get_platform():
    platforms = {'linux1': 'Linux', 
     'linux2': 'Linux', 
     'darwin': 'OS X', 
     'win32': 'Windows'}
    if sys.platform not in platforms:
        raise ValueError('Unsupported OS: %s' % sys.platform)
    return platforms[sys.platform]


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    skip_flag = False if sys.platform == 'win32' else True

    def signal_handler(signum, frame):
        raise TimeoutException('Timed out!')

    if skip_flag:
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
    try:
        yield
    finally:
        if skip_flag:
            signal.alarm(0)