# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/timings.py
# Compiled at: 2012-06-19 11:02:04


class Timings(object):

    def __init__(self, j):
        self.raw = j
        if 'blocked' in self.raw:
            self.blocked = self.raw['blocked']
        else:
            self.blocked = -1
        if 'dns' in self.raw:
            self.dns = self.raw['dns']
        else:
            self.dns = -1
        if 'connect' in self.raw:
            self.connect = self.raw['connect']
        else:
            self.connect = -1
        self.send = self.raw['send']
        self.wait = self.raw['wait']
        self.receive = self.raw['receive']
        if 'ssl' in self.raw:
            self.ssl = self.raw['ssl']
        else:
            self.ssl = -1
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''