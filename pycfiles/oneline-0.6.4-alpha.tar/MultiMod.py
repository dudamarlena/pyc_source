# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/oneline/modules/MultiMod.py
# Compiled at: 2015-03-28 13:51:27
from oneline import ol
import GeoMod

class MultiMod(ol.module):

    def start(self):
        db = ol.storage()
        geo = ol.geo()
        ev = ol.event()
        print 'Changing the order of geo and ev '
        self.pipeline = ol.stream(pline=[ev, geo], db=db)

    def receiver(self, message):
        self.pipeline.run(message)

    def upstream(self, message):
        geo = GeoMod()
        geo.open()

    def provider(self, message):
        self.pipeline.run(message)

    def end(self):
        print 'closing multimod :('
        del self.pipeline