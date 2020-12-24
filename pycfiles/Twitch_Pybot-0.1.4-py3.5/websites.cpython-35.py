# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybot/filters/websites.py
# Compiled at: 2016-07-13 16:56:07
# Size of source mod 2**32: 614 bytes
import sys, random, re

def raw_string(s):
    if isinstance(s, str):
        s = s.encode('string-escape')
    elif isinstance(s, unicode):
        s = s.encode('unicode-escape')
    return s


name = sys.argv[0]
msg = sys.argv[1]
REGEX = re.compile('((ftp|http|https):\\/\\/)?([a-zA-Z0-9]+(\\.[a-zA-Z0-9]+)+.*)', re.IGNORECASE)
KICK_MSGS = ['please dont post links without permission.', 'please ask before posting a link.']
if REGEX.search(msg) is not None:
    pybotPrint('[FILTER][WEBSITES.PY] ' + name, 'filter')
    self.kick(name)
    self.msg(name + ' ' + KICK_MSGS[random.randint(0, len(KICK_MSGS) - 1)])