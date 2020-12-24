# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/ask.py
# Compiled at: 2014-07-11 17:28:38


def ask(q, ans):
    lowans = map(str.lower, ans)
    req = ('{0} ({1}) ').format(q, ('/').join(lowans))
    while True:
        r = raw_input(req).lower().strip()
        if r in ans:
            return r