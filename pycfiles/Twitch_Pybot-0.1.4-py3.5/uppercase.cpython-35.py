# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/filters/uppercase.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 583 bytes
import sys, random
MIN_MSG_LEN = 7
KICK_MSGS = ['please dont yell',
 "i'll cut you if you keep yelling"]
name = sys.argv[0]
msg = sys.argv[1]
if len(msg) >= MIN_MSG_LEN and msg.isupper():
    pybotPrint('[FILTER][UPPERCASE.PY] ' + name, 'filter')
    self.msg(name + ' ' + KICK_MSGS[random.randint(0, len(KICK_MSGS) - 1)])
    self.kick(name)