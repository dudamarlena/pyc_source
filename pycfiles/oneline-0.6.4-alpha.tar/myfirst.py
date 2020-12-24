# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/oneline/modules/myfirst.py
# Compiled at: 2015-01-18 16:34:18
from oneline import ol

class myfirst(ol.module):

    def start(self):
        self.pipeline = ol.stream()

    def receiver(self, message):
        self.pipeline.run(message)