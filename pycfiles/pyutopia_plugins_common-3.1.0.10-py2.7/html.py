# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/html.py
# Compiled at: 2017-06-15 12:59:20
import urllib2, utopia.citation
from lxml import etree
from StringIO import StringIO

class HTMLResolver(utopia.citation.Resolver):
    """Resolve PDF link from an article's web page"""

    def resolve(self, citations, document=None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'html'}):
            article_links = utopia.citation.filter_links(citations, {'type': 'article', 'mime': 'text/html'})
            for article_link in article_links:
                url = article_link['url']
                parser = etree.HTMLParser()
                try:
                    request = urllib2.Request(url, headers={'Accept-Content': 'gzip'})
                    resource = urllib2.urlopen(request, timeout=12)
                except urllib2.HTTPError as e:
                    if e.getcode() == 401:
                        resource = e
                    else:
                        raise

                html = resource.read()
                article_link['resolved_url'] = resource.geturl()
                dom = etree.parse(StringIO(html), parser)
                citations_pdf_urls = dom.xpath('/html/head/meta[@name="citations_pdf_url"]/@content')
                for pdf_url in citations_pdf_urls:
                    if pdf_url != resource.geturl():
                        citation.setdefault('links', [])
                        citation['links'].append({'url': pdf_url, 
                           'mime': 'application/pdf', 
                           'type': 'article', 
                           'title': 'Download article'})

        return citation

    def provenance(self):
        return {'whence': 'html'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 102