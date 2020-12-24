# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/socialize/socialize/services/kickstarter_service.py
# Compiled at: 2016-10-19 09:13:43
from .service import Service

class KickstarterService(Service):

    def get_supporters(self):
        r = self.get('kickstarter/')
        self.print_supporters(r)

    def print_supporters(self, s):
        for supporter in s:
            print '%-40s %s' % (str(supporter['name']), str(supporter['message']))


kick = KickstarterService()