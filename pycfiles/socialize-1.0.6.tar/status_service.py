# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/socialize/socialize/services/status_service.py
# Compiled at: 2016-10-19 09:13:43
from .service import Service

class StatusService(Service):

    def get_feed(self):
        r = self.get('status/feed/')
        print ''
        for status in r:
            self.print_status(status)

        print ''

    def post_status(self, message):
        r = self.post('status/', data={'message': str(message)})
        self.check_reponse(r, success='Successfully posted a new status')

    def print_status(self, status):
        print str(status['username']) + '> ' + str(status['message'])


statusmanagement = StatusService()