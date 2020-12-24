# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/sigwinch_report.py
# Compiled at: 2011-11-02 15:34:08
import signal, time, struct, fcntl, termios, os, sys

def getwinsize():
    """This returns the window size of the child tty.
    The return value is a tuple of (rows, cols).
    """
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]


def handler(signum, frame):
    print('signal')
    sys.stdout.flush()
    print('SIGWINCH:', getwinsize())
    sys.stdout.flush()


print('setting handler for SIGWINCH')
signal.signal(signal.SIGWINCH, handler)
while True:
    sys.stdout.flush()
    time.sleep(1)