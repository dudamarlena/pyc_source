# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/filters/repetition.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 629 bytes
import sys, random
name = sys.argv[0]
msg = sys.argv[1]
db = self.accessDb('rep_db')
REP_AMMOUNT = 3
KICK_MSGS = [
 "please don't repeat yourself.", "don't repeat yourself"]
try:
    if msg.lower().strip() == db[name][0].lower().strip():
        db[name][1] += 1
        if db[name][1] >= REP_AMMOUNT:
            pybotPrint('[FILTER][REPETITION.PY] ' + name, 'filter')
            self.msg(name + ' ' + KICK_MSGS[random.randint(0, len(KICK_MSGS) - 1)])
            self.kick(name)
    else:
        db[name][0] = msg
        db[name][1] = 1
except:
    db[name] = [
     msg, 1]