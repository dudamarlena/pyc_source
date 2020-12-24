# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/completion.py
# Compiled at: 2011-12-19 12:23:48


class Completion(object):

    def __init__(self):
        self.nicks = []

    def add(self, nick):
        if nick not in self.nicks:
            self.nicks.append(nick)

    def __repr__(self):
        return str(self.nicks)

    def __len__(self):
        return len(self.nicks)

    def complete(self, word):
        nick = []
        for n in self.nicks:
            if word in n:
                nick.append(n)

        if len(nick) is 1:
            return nick[0]
        else:
            return
            return

    def text_complete(self, text):
        """Return the text to insert"""
        t = text.split(' ')
        last = t[(-1)]
        if last[0] is '@':
            nick = self.complete(last[1:])
            if nick:
                return nick[len(last) - 1:]
        return