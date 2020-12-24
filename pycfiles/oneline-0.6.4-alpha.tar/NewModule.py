# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/modules/NewModule.py
# Compiled at: 2014-08-25 13:28:25
from oneline import ol

class NewModule(ol.module):

    def start(self):
        print 'i am opening a connection!'
        self.pipeline = ol.stream()

    def receiver(self, message):
        print 'i am receiving data'
        self.pipeline.run(message)

    def provider(self, message):
        print 'i am providing data!'

    def end(self):
        print 'i am closing a connection and cleaning up your leftover data'
        del self.pipeline