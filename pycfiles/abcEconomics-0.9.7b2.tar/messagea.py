# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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