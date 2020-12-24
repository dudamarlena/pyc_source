# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /oneline/modules/BurgerMod.py
# Compiled at: 2014-12-05 17:32:31
from oneline import ol

class BurgerMod(ol.module):

    def start(self):
        """ starting chat module """
        self.pipeline = ol.stream()
        print 'connected: ' + self.unique

    def receiver(self, message):
        self.pipeline.run(message)

    def provider(self, message):
        self.pipeline.broadcast('testing')

    def provider(self, message):
        pass