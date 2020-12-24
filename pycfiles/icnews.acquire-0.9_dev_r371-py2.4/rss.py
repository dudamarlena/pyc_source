# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/acquire/browser/rss.py
# Compiled at: 2008-10-06 10:31:17
"""Defines the RSS2 views
"""
import sys, datetime, urlparse
from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five.browser import BrowserView
from icnews.acquire.interfaces import IAdqnewsDB, INewsFromURL
from icnews.acquire.interfaces import IicNewsManagementAcquireSQLServer

class BaseRSS2View(BrowserView):
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def rss2(self, news):
        u"""Genera un contenido rss a partir de una url y una expresión
        regular. La expresión regular (regexp) debe tener grupos de
        matching nombrados como:
        title: titulo de la noticia.
        link: url que nos lleva a la noticia
        description: descripción de la noticia.

        El title (titulo) de la función corresponde al titulo del canal
        rss de donde se saco la noticia. También hay que definir la url
        (link) de la página a parsear, y una descripción del canal
        (description). Muchas páginas no tienen definido la
        codificación de los caracteres (encoding), con lo que es
        recomendable asigarnle uno.
        """
        context = aq_inner(self.context)
        title = context.Title()
        link = context.getSource()
        description = context.Description()
        encoding = context.getEncoding()
        l = news
        s = '<?xml version="1.0" encoding="%s"?>\n<rss version="2.0">\n  <channel>\n    <title>%s</title>\n    <link>%s</link>\n    <description>%s</description>\n' % (encoding, unicode(title, sys.stdin.encoding), unicode(link, sys.stdin.encoding), unicode(description, sys.stdin.encoding))
        for si in l:
            if 'title' in si and si['title']:
                s += '  <item>\n'
                s += '     <title>%s</title>\n' % si['title'].decode(encoding)
                if 'link' in si and si['link']:
                    s += '     <link>%s</link>\n' % urlparse.urljoin(link, si['link'])
                if 'description' in si and si['description']:
                    s += '     <description>%s</description>\n' % si['description'].decode(encoding)
                s += '  </item>\n'

        s += '\n  </channel>\n</rss>'
        return s


class RSS2View(BaseRSS2View):
    """RSS2 view generated on the fly"""
    __module__ = __name__

    def __call__(self):
        """Use the RSS2 adapter to return the RSS2"""
        response = self.request.response
        response.setHeader('Content-Type', 'text/xml')
        if self.context.getStore():
            dba = IAdqnewsDB(self.context)
            news = dba.store()
        else:
            news = INewsFromURL(self.context)
        return self.rss2(news)


class StoredNews(BaseRSS2View):
    """RSS2 view generated from the DB"""
    __module__ = __name__

    def __call__(self):
        """Use the RSS2 adapter to return the RSS2 from DB"""
        response = self.request.response
        response.setHeader('Content-Type', 'text/xml')
        dba = IAdqnewsDB(self.context)
        news = dba.retrieve(datetime.date.today())
        return self.rss2(news)