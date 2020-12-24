# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/oneline/modules/MemcachedMod.py
# Compiled at: 2015-03-28 13:51:27
from oneline import ol

class MemcachedMod(ol.module):

    def start(self):
        """ starting chat module """
        self.pipeline = ol.stream()
        print 'Running module: ' + self.__str__()

    def receiver(self, message):
        self.pipeline.run(message)

    def provider(self, message):
        pass

    def end(self):
        print 'Closing module: ' + self.__str__()