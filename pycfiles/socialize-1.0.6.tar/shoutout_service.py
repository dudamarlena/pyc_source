# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dominicmonn/Documents/Private/socialize/socialize/services/shoutout_service.py
# Compiled at: 2016-10-19 09:13:43
from .service import Service

class ShoutService(Service):

    def get_feed(self):
        r = self.get('shoutout/feed/')
        print ''
        for status in r:
            self.print_shouts(status)

        print ''

    def post_status(self, message, anon=False):
        if anon:
            print 'Posting Shoutout as Anonymous'
        r = self.post('shoutout/', data={'message': str(message), 'anon': anon})
        self.check_reponse(r, success='Successfully posted a new shoutout')

    def print_shouts(self, status):
        print str(status['username']) + '> ' + str(status['message'])


shoutouts = ShoutService()