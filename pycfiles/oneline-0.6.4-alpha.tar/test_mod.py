# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/oneline/modules/test_mod.py
# Compiled at: 2015-01-18 14:40:57
from oneline import ol

class test_mod(ol.module):

    def start(self):
        print 'Opening echo module'
        self.pipeline = ol.stream()

    def receiver(self, message):
        self.pipeline.run(message)

    def provider(self, message):
        self.pipeline.run(message)

    def end(self, message):
        pass