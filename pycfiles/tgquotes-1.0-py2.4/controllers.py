# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgquotes\controllers.py
# Compiled at: 2006-12-11 15:42:37
import turbogears
from turbogears import controllers, expose, redirect
import urllib, simplejson
from tgquotes import json

class QuoteController(controllers.Controller):
    __module__ = __name__

    @expose('json')
    def index(self):
        import model
        return dict(quotes=model.Quote.random())

    @expose('json')
    def default(self, *args, **kw):
        import model
        try:
            num = int(args[0])
            return dict(quotes=model.Quote.random(num))
        except ValueError, TypeError:
            return dict(quotes=[])


class QuoteProxyController(controllers.Controller):
    __module__ = __name__

    def __init__(self, host, *args, **kw):
        self.host = host
        super(controllers.Controller, self).__init__(*args, **kw)

    @expose('json')
    def index(self):
        quotes = urllib.urlopen(self.host)
        return dict(quotes=simplejson.load(quotes)['quotes'])

    @expose('json')
    def default(self, *args, **kw):
        try:
            quotes = urllib.urlopen('%s/%s' % (self.host, args[0]))
            quotes = simplejson.load(quotes)['quotes']
        except ValueError:
            quotes = []

        return dict(quotes=quotes)


class Root(controllers.RootController):
    __module__ = __name__

    @expose(template='tgquotes.templates.welcome')
    def index(self):
        import time
        return dict(now=time.ctime())

    quote = QuoteController()