# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /a/lib/python3.6/site-packages/bibtools/fetchpdf.py
# Compiled at: 2017-05-31 09:41:18
# Size of source mod 2**32: 7350 bytes
"""
Downloading PDFs automagically.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import io, os, re
from hashlib import sha1
from .util import *
from . import webutil as wu
__all__ = 'try_fetch_pdf'.split()

def try_fetch_pdf(proxy, destpath, arxiv=None, bibcode=None, doi=None, max_attempts=5):
    """Given reference information, download a PDF to a specified path. Returns
    the SHA1 sum of the PDF as a hexadecimal string, or None if we couldn't
    figure out how to download it."""
    pdfurl = None
    if doi is not None:
        jurl = doi_to_journal_url(doi)
        print('[Attempting to scrape', jurl, '...]')
        try:
            pdfurl = proxy.unmangle(scrape_pdf_url(proxy.open(jurl)))
        except wu.HTTPError as e:
            warn('got HTTP error %s (%s) when trying to fetch %s', e.code, e.reason, e.url)
            return

    if pdfurl is None:
        if bibcode is not None:
            pdfurl = bibcode_to_maybe_pdf_url(bibcode)
    if pdfurl is None:
        if arxiv is not None:
            pdfurl = 'http://arxiv.org/pdf/' + wu.urlquote(arxiv) + '.pdf'
    if pdfurl is None:
        return
    else:
        attempts = 0
        resp = None
        while attempts < max_attempts:
            attempts += 1
            print('[Trying', pdfurl, '...]')
            try:
                resp = proxy.open(pdfurl)
            except wu.HTTPError as e:
                if e.code == 404:
                    if wu.urlparse(pdfurl)[1] == 'articles.adsabs.harvard.edu':
                        warn("ADS doesn't actually have the PDF on file")
                        return try_fetch_pdf(proxy, destpath, arxiv=arxiv, bibcode=None, doi=doi)
                warn('got HTTP error %s (%s) when trying to fetch %s', e.code, e.reason, e.url)
                return

            if resp.getheader('Content-Type', 'undefined').startswith('text/html'):
                pdfurl = proxy.unmangle(scrape_pdf_url(resp))
                resp = None
                if pdfurl is None:
                    warn("couldn't find PDF link")
                    return
            else:
                break

        if resp is None:
            warn('too many links when trying to find actual PDF')
            return
        s = sha1()
        first = True
        with io.open(destpath, 'wb') as (f):
            while True:
                b = resp.read(4096)
                if first:
                    if len(b) < 4 or b[:4] != b'%PDF':
                        warn('response does not seem to be a PDF')
                        resp.close()
                        f.close()
                        os.unlink(destpath)
                        return
                    first = False
                if not len(b):
                    break
                s.update(b)
                f.write(b)

        return s.hexdigest()


class PDFUrlScraper(wu.HTMLParser):
    __doc__ = 'Observed places to look for PDF URLs:\n\n    <meta> tag with name=citation_pdf_url -- IOP\n    <a> tag with id=download-pdf -- Nature (non-mobile site, newer)\n    <a> tag with class=download-pdf -- Nature (older)\n    <a> tag with class=pdf -- AIP\n    <a> tag with \'pdf-button-main\' in class -- IOP through Harvard proxy\n    <a> tag with id=pdfLink -- ScienceDirect\n    <iframe id="pdfDocument" src="..."> -- Wiley Online Library, inner PDF wrapper\n    '
    _bad_iop_cpu = re.compile('.*iopscience\\.iop\\.org.*/pdf.*pdf$')

    def __init__(self, cururl):
        wu.HTMLParser.__init__(self)
        self.cururl = cururl
        self.pdfurl = None

    def maybe_set_pdfurl(self, url):
        url = wu.urljoin(self.cururl, url)
        if url != self.cururl:
            self.pdfurl = url

    def handle_starttag(self, tag, attrs):
        if self.pdfurl is not None:
            return
        if tag == 'meta':
            attrs = dict(attrs)
            if attrs.get('name') == 'citation_pdf_url':
                url = attrs['content']
                if not self._bad_iop_cpu.match(url):
                    self.maybe_set_pdfurl(url)
        else:
            if tag == 'a':
                attrs = dict(attrs)
                if attrs.get('id') == 'download-pdf':
                    self.maybe_set_pdfurl(attrs['href'])
                else:
                    if attrs.get('id') == 'pdfLink':
                        self.maybe_set_pdfurl(attrs['href'])
                    else:
                        if attrs.get('class') == 'download-pdf':
                            self.maybe_set_pdfurl(attrs['href'])
                        else:
                            if attrs.get('class') == 'pdf':
                                self.maybe_set_pdfurl(attrs['href'])
                            else:
                                if 'pdf-button-main' in attrs.get('class', ''):
                                    self.maybe_set_pdfurl(attrs['href'])
                                else:
                                    if (attrs.get('href') or '').endswith('?acceptTC=true'):
                                        self.maybe_set_pdfurl(attrs['href'])
            elif tag == 'iframe':
                attrs = dict(attrs)
                if attrs.get('id') == 'pdfDocument':
                    self.maybe_set_pdfurl(attrs['src'])


def scrape_pdf_url(resp):
    return wu.parse_http_html(resp, PDFUrlScraper(resp.url)).pdfurl


def doi_to_journal_url(doi):
    return wu.get_url_from_redirection('http://dx.doi.org/' + wu.urlquote(doi))


def bibcode_to_maybe_pdf_url(bibcode):
    """If ADS doesn't have a fulltext link for a given bibcode, it will return a link
    to articles.ads.harvard.edu that in turn yields an HTML error page.

    Also, the Location header returned by the ADS server appears to be slightly broken,
    with the &'s in the URL being HTML entity-encoded to &amp;s."""
    url = 'http://adsabs.harvard.edu/cgi-bin/nph-data_query?link_type=ARTICLE&bibcode=' + wu.urlquote(bibcode)
    pdfurl = wu.get_url_from_redirection(url)
    return pdfurl.replace('&amp;', '&')