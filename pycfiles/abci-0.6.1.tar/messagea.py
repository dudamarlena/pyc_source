# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/taghawi/Dropbox/workspace/abce/unittest/messagea.py
# Compiled at: 2017-12-13 07:05:30
from __future__ import division
import abce

class MessageA(abce.Agent):

    def init(self):
        pass

    def sendmsg(self):
        self.send(('messageb', self.id), 'msg', 'hello there')

    def recvmsg(self):
        assert self.get_messages('msg')[0].content == 'hello there'