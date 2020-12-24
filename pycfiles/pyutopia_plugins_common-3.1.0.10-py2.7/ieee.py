# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/plugins/common/ieee.py
# Compiled at: 2017-06-15 12:59:20
import urllib2, urlparse, utopia.citation
from lxml import etree
from StringIO import StringIO

class IEEEResolver(utopia.citation.Resolver):
    """Resolve PDF link from an IEEE page"""

    def resolve(self, citations, document=None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'ieee'}):
            resolved_links = utopia.citation.filter_links(citations, {'resolved_url': None})
            for link in resolved_links:
                url = link['resolved_url']
                if 'ieeexplore.ieee.org' in url:
                    parser = etree.HTMLParser()
                    resource = urllib2.urlopen(url, timeout=12)
                    html = resource.read()
                    dom = etree.parse(StringIO(html), parser)
                    download_pdf_urls = dom.xpath('//a[@id="full-text-pdf"]/@href')
                    for pdf_url in download_pdf_urls:
                        pdf_url = urlparse.urljoin(url, pdf_url)
                        if pdf_url != resource.geturl():
                            resource = urllib2.urlopen(pdf_url, timeout=12)
                            html = resource.read()
                            dom = etree.parse(StringIO(html), parser)
                            download_pdf_urls = dom.xpath("//frame[contains(@src, 'pdf')]/@src")
                            for pdf_url in download_pdf_urls:
                                pdf_url = urlparse.urljoin(url, pdf_url)
                                citation.setdefault('links', [])
                                citation['links'].append({'url': pdf_url, 
                                   'mime': 'application/pdf', 
                                   'type': 'article', 
                                   'title': 'Download article from IEEEXplore'})

        return citation

    def provenance(self):
        return {'whence': 'ieee'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 103