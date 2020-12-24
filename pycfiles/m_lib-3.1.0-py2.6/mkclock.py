# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/clock/mkclock.py
# Compiled at: 2016-07-25 12:10:56
"""Test if current interpreter do not have clock() and define it as need"""
from __future__ import print_function
import sys, time
print('Testing...', end=' ')
sys.stdout.flush()
time.sleep(3)
print('\n' + ' ' * len('Testing...') + '\n', end=' ')
need_clock = time.clock() != 3
outfile = open('clock.py', 'w')
if need_clock:
    print('Generaing clock.py with custom clock()')
    outfile.write('"""\n   Define clock() for systems that do not have it\n"""\n\nfrom time import time\n_clock = time()\n\ndef clock():\n   return int(time() - _clock)\n')
else:
    print('Generaing clock.py with standard clock()')
    outfile.write('"""\n   Define clock() shim\n"""\n\nfrom time import clock\n   ')