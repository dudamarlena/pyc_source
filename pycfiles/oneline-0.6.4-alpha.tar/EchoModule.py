# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/modules/EchoModule.py
# Compiled at: 2014-08-25 13:39:58
from oneline import ol

class EchoModule(ol.module):

    def start(self):
        self.pipeline = ol.stream()

    def receiver(self, message):
        self.pipeline.run(message)

    def provider(self, message):
        pass

    def end(self):
        print 'bye bye'