# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erik/Develop/amlo/src/iservices.rssdocument/iservices/rssdocument/browser/rsscode.py
# Compiled at: 2012-05-04 01:12:57
from Acquisition import aq_inner
from Products.Five.browser import BrowserView

class rsscodeView(BrowserView):
    js_code = "$(document).ready(function () {$('#rsscontainer-%s').rssfeed('%s', {limit: %s});});"

    def __call__(self, REQUEST, RESPONSE):
        context = aq_inner(self.context)
        RESPONSE.setHeader('Content-Type', 'application/javascript')
        return self.js_code % (context.UID(), context.getRSSLink(), context.getMax_entries())