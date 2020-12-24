# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/ask.py
# Compiled at: 2014-07-11 17:28:38


def ask(q, ans):
    lowans = map(str.lower, ans)
    req = ('{0} ({1}) ').format(q, ('/').join(lowans))
    while True:
        r = raw_input(req).lower().strip()
        if r in ans:
            return r