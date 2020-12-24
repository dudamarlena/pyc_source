# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/echo_wait.py
# Compiled at: 2011-11-02 15:34:08
import signal, time, struct, fcntl, termios, os, sys
print('fake password:')
sys.stdout.flush()
time.sleep(3)
attr = termios.tcgetattr(sys.stdout)
attr[3] = attr[3] & ~termios.ECHO
termios.tcsetattr(sys.stdout, termios.TCSANOW, attr)
time.sleep(12)
attr[3] = attr[3] | termios.ECHO
termios.tcsetattr(sys.stdout, termios.TCSANOW, attr)
time.sleep(2)