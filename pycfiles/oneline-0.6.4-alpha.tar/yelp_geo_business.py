# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/oneline/modules/yelp_geo_business.py
# Compiled at: 2015-03-28 20:29:13
from oneline import ol

class yelp_geo_business(ol.module):

    def start(self):
        print 'starting yelp module'
        self.pipeline = ol.stream()

    def provider(self, message):
        return self.pipeline.run(message)

    def receiver(self, message):
        data = ol.parse_message(message)
        return self.pipeline.run(message)

    def stop(self):
        print 'closing  Yelp module'