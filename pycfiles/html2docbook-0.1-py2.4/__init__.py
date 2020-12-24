# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/html2docbook/__init__.py
# Compiled at: 2009-03-11 15:49:10
import os, sys, re
from htmlentitydefs import name2codepoint
from lxml import etree
from BeautifulSoup import BeautifulSoup
_debug = False

class Html2DocBook(object):
    """Transform HTML to DocBook XML.
    """
    __module__ = __name__

    def __init__(self, cleanup=False, verbose=False):
        self.cleanup = cleanup
        self.verbose = verbose
        xsl_html2docbook = os.path.abspath(os.path.join(os.path.dirname(__file__), 'html2docbook.xsl'))
        if not os.path.exists(xsl_html2docbook):
            raise IOError('%s does not exist' % xsl_html2docbook)
        self.xsl_html2docbook = xsl_html2docbook

    def handler(self, mo):
        """Replace all HTML entities with the corresponding numeric entities.
        """
        e = mo.group(1)
        v = e[1:-1]
        if not v.startswith('#'):
            codepoint = name2codepoint.get(v)
            return codepoint and '&#%d;' % codepoint or ''
        else:
            return e

    def transform(self, html):
        """Transform the HTML input into DocBook XML.
        """
        html = '<html><body>%s</body></html>' % html
        if _debug:
            print 'HTML Input:\n%s' % html
        html = html.replace(' & ', ' &amp; ')
        if _debug:
            print 'HTML & Replace:\n%s' % html
        soup = BeautifulSoup(html)
        for img in soup.findAll('img'):
            src = img['src']
            if not os.path.exists(src):
                raise IOError('No image file found: %s' % src)

        html = str(soup)
        if _debug:
            print 'Beautiful Soup:\n%s' % html
        entity_reg = re.compile('(&.*?;)')
        html = entity_reg.sub(self.handler, html)
        if _debug:
            print 'Replace HTML entities:\n%s' % html
        try:
            parser = etree.XMLParser(recover=True, remove_blank_text=True)
            htmltree = etree.XML(html, parser)
            styletree = etree.parse(self.xsl_html2docbook)
            transform = etree.XSLT(styletree)
            resulttree = transform(htmltree)
            if _debug:
                print 'DocBook:\n%s' % etree.tostring(resulttree)
            for element in resulttree.iter('*'):
                if element.text is not None and not element.text.strip():
                    element.text = None

            if _debug:
                print 'DocBook after striping inner whitespace:\n%s' % etree.tostring(resulttree)
            docbook = etree.tostring(resulttree)
        except:
            print >> sys.stderr, 'Error transforming %s' % html
            raise

        return docbook