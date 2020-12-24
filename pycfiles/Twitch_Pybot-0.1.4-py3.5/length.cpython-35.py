# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/filters/length.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 387 bytes
import sys, random
name = sys.argv[0]
msg = sys.argv[1]
MAX_CHAR_LEN = 250
KICK_MSGS = [
 'your message was too long, please split it up into multiple parts.', 'please split your message into multiple parts.']
if len(msg) > MAX_CHAR_LEN:
    pybotPrint('[FILTER][LENGTH.PY] ' + name, 'red')
    self.kick(name)
    self.msg(name + ' ' + KICK_MSGS[random.randint(0, len(KICK_MSGS) - 1)])