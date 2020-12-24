# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/xtemplate/xtemplate.py
# Compiled at: 2007-08-25 13:41:36
from zope.publisher.browser import BrowserPage
from zope.traversing.browser.absoluteurl import absoluteURL
import logging
from zope.publisher.http import getCharsetUsingRequest, IResult
from zope.publisher.interfaces.browser import IBrowserRequest
import os
from StringIO import StringIO
import time
from xml.dom import XHTML_NAMESPACE, XML_NAMESPACE
logger = logging.getLogger()
from sanitizer import HTMLSanitizer
from interfaces import ILXMLHTMLPage
from zope.interface import implements
from zope.component import adapts
try:
    from lxml.etree import Element, SubElement, tounicode, ElementTree, fromstring, XMLSyntaxError, HTML, Comment, parse, HTMLParser, XMLParser
except ImportError:
    print 'This package uses lxml.(http://codespeak.net/lxml/) \n    It may be installed as "lxml" or "python-lxml" in Linux distributions.\n    easy_install also works.  You want version 1.0+\n    '
    raise

from lxmlhtmlutils import getElementById, appendSnippet, appendWidget, fixEmptyElements, fixTDs
localfilepath = os.path.dirname(__file__)
baseTemplate = os.path.join(localfilepath, 'basetemplate.html')
t_doc_type = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
doc_type = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'

def readLocalFile(filename):
    filepath = os.path.join(localfilepath, filename)
    if os.path.isfile(filepath):
        return file(filepath).readlines()
    raise ValueError('Could not read file %s' % filepath)


class XTemplate(BrowserPage):
    __module__ = __name__
    implements(ILXMLHTMLPage)
    defaultTitle = 'Untitled'
    lang = 'en'
    strictXHTML = True
    useMetaContentTypeTag = True
    cacheControl = True
    title = ''
    docTypeHeader = True
    prettyPrint = True
    tdFix = False
    benchmark = True
    generatorTag = True
    IE = False
    KHTML = False
    Gecko = False

    def __init__(self, context, request):
        """Initialize the page"""
        super(XTemplate, self).__init__(context, request)
        agent = self.request.get('HTTP_USER_AGENT', '')
        if 'MSIE' in agent:
            self.IE = True
        if 'KHTML' in agent:
            self.KHTML = True
        if 'Gecko' in agent:
            self.Gecko = True
        self.agent = agent
        self.startTime = time.time()
        template = self.getTemplate()
        if template is None:
            baseTemplate = os.path.join(localfilepath, 'basetemplate.html')
            z = open(baseTemplate).read()
            template = z
        if template:
            s = StringIO(template)
            parser = XMLParser(remove_blank_text=True)
            self.document = parse(s, parser)
            self.docElement = self.document.getroot()
            self.head = self.document.xpath('//head')[0]
            self.body = self.document.xpath('//body')[0]
        else:
            self.docElement = Element('html')
            self.document = ElementTree(self.docElement)
            self.head = SubElement(self.docElement, 'head')
            self.body = SubElement(self.docElement, 'body')
        self.scripts = []
        self.styleSheets = []
        self.charset = getCharsetUsingRequest(request)
        return

    def getTemplate(self):
        """return a string or unicode representation of the base HTML template
        for this template.  Override this if you want to use a different
        template provider.  Base implementation here returns None
        """
        return

    def renderDocBoilerPlate(self):
        self.docElement.set('xmlns', XHTML_NAMESPACE)
        self.docElement.set('{%s}lang' % XML_NAMESPACE, self.lang)
        self.docElement.set('lang', self.lang)
        ca = self.request.environment.get('HTTP_ACCEPT', '')
        if self.strictXHTML:
            if 'application/xhtml+xml' in ca:
                ct = 'application/xhtml+xml'
                self.request.response.setHeader('content-type', '%s' % ct)
            else:
                self.strictXHTML = False
        if not self.strictXHTML:
            ct = 'text/html'
            self.request.response.setHeader('content-type', '%s;charset=%s' % (ct, self.charset))
        if self.useMetaContentTypeTag:
            self.addMetaTag({'http-equiv': 'content-type', 'content': '%s;charset=%s' % (ct, self.charset)})
        self.renderMetaTags()
        if self.cacheControl:
            self.doCacheControl()

    def doCacheControl(self):
        """cache control.
            may be overriden in descendents.
            set cacheControl to True to invoke"""
        self.request.response.setHeader('cache-control', 'no-cache')

    def renderTitle(self, getTitle=None):
        """obtain title from ... somewhere..."""
        tt = SubElement(self.head, 'title')
        if getTitle:
            try:
                tt.text = getTitle()
            except TypeError:
                tt.text = getTitle

        elif self.title:
            tt.text = self.title
        else:
            try:
                tt.text = self.getTitle()
            except AttributeError:
                try:
                    tt.text = self.context.getTitle()
                except AttributeError:
                    tt.text = self.defaultTitle

    def renderMetaTags(self):
        if self.generatorTag:
            self.addMetaTag({'name': 'generator', 'content': 'zif.xtemplate'})
        self.addMetaTag({'http-equiv': 'Content-Style-Type', 'content': 'text/css'})

    def addMetaTag(self, attribs):
        """ add a meta tag. attribs is a dict"""
        tag = Element('meta', attribs)
        self.head.append(tag)

    def render(self):
        """Descendent classes should override this.
        available elements;
        self.body
        self.head
        self.docElement
        These are lxml.etree.Elements that have the elementtree api.
        """
        pass

    def getElementById(self, anId):
        """return the first element with this id attribute.
        Return None if not available"""
        return getElementById(self.docElement, anId)

    def appendSnippet(self, target, s, sanitize=True):
        """apppend the snippet at target
        target is an Element in the document.
        s is the snippet, a string of xml.  It does not need to have any tags, 
        if the snippet is otherwise not well-formed or understood as XML, 
        it will be parsed by lxml.HTML as tag soup.
        snippet will be appended to text and/or children of the location Element.
        """
        appendSnippet(target, s, sanitize=True)

    def appendWidget(self, target, widget):
        appendWidget(target, widget)

    def renderStyleSheetsAndScripts(self):
        """do script and style tags"""
        for k in self.scripts:
            s = SubElement(self.head, 'script', {'type': 'text/javascript'})
            s.set('src', k)

        for k in self.styleSheets:
            s = SubElement(self.head, 'link', {'rel': 'stylesheet', 'type': 'text/css', 'href': k})

    def postProcess(self):
        """perform subclass-specific post-processing"""
        pass

    def fixEmptyElements(self):
        """globally make a fix on empty elements for the dtd.
        lxml likes to xml-minimize if possible.  Here we assign some 
        (empty) text so this does not happen when it should not."""
        fixEmptyElements(self.docElement)

    def fixTDs(self):
        """set td text non-none so pretty-print does not add extra space"""
        fixTDs(self.body)

    def fixForms(self):
        """set action and method on forms if missing"""
        forms = self.body.xpath('//form')
        for form in forms:
            action = form.get('action')
            if not action:
                action = self.request['PATH_INFO']
                form.set('action', action)
            method = form.get('method')
            if not method:
                form.set('method', 'post')

    def renderEndComment(self):
        """override this if want something different..."""
        s = Comment('Created with Zope 3 XTemplate')
        self.docElement.append(s)

    def finalizePage(self):
        self.renderTitle()
        self.renderDocBoilerPlate()
        self.fixForms()
        self.renderStyleSheetsAndScripts()
        self.fixEmptyElements()
        self.postProcess()
        if self.tdFix and self.prettyPrint:
            self.fixTDs()

    def addScript(self, url):
        """add a script url"""
        if url not in self.scripts:
            self.scripts.append(url)

    def addStyleSheet(self, url):
        """add a style sheet url"""
        if url not in self.styleSheets:
            self.styleSheets.append(url)

    def __call__(self):
        self.render()
        self.finalizePage()
        doc = tounicode(self.document, pretty_print=self.prettyPrint)
        if not self.strictXHTML:
            dt = t_doc_type
        else:
            dt = doc_type
        txt = doc.encode(self.charset)
        if not self.strictXHTML:
            replacements = (('/>', ' />'), ('&apos;', '&#39;'))
            for m in replacements:
                if m[0] in txt:
                    txt = txt.replace(m[0], m[1])

        output = [
         txt]
        if self.docTypeHeader:
            output.append(dt)
        if self.strictXHTML:
            xmlheader = '<?xml version="1.0" encoding="%s"?>' % self.charset
            output.append(xmlheader)
        e = ('\n').join(reversed(output))
        if self.benchmark:
            logger.log(logging.INFO, 'Page generated in %01.4f s.' % (time.time() - self.startTime,))
        return e

    def asSnippet(self, element=None, pretty_print=True):
        """return an element and its contents as unicode string.
        no post-processing here.  Subclasses are free to first call 
        other routines in e.g., finalizePage, if desired.
        """
        if not element:
            element = self.body
        doc = tounicode(element, pretty_print=pretty_print)
        return doc