# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/transforms/outputfilter.py
# Compiled at: 2013-12-24 05:41:42
from zope.interface import implements, Interface
from plone.transformchain.interfaces import ITransform
try:
    from plone.app.theming.interfaces import IThemingLayer
except ImportError:
    from zope.interface import Interface as IThemingLayer

from zope.component import adapts
import newrelic.agent
from lxml import etree
from repoze.xmliter.utils import getHTMLSerializer
from collective.newrelic.patches.zserverpublisher import PLACEHOLDER

class NewRelic(object):
    """Outputfilter that adds NewRelic Real User Monitoring to content.

    Late stage in the 8000's transform chain. When plone.app.blocks is
    used, we can benefit from lxml parsing having taken place already.
    """
    implements(ITransform)
    adapts(Interface, IThemingLayer)
    order = 8860

    def __init__(self, context=None, request=None):
        self.context = context
        self.request = request

    def parseTree(self, result):
        contentType = self.request.response.getHeader('Content-Type')
        if contentType is None or not contentType.startswith('text/html'):
            return
        else:
            contentEncoding = self.request.response.getHeader('Content-Encoding')
            if contentEncoding and contentEncoding in ('zip', 'deflate', 'compress'):
                return
            try:
                return getHTMLSerializer(result, pretty_print=False)
            except (TypeError, etree.ParseError):
                return

            return

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformIterable(self, result, encoding):
        result = self.parseTree(result)
        if result is None:
            return
        else:
            trans = newrelic.agent.current_transaction()
            if trans is None:
                return result
            if trans.name == PLACEHOLDER:
                return result
            head = result.tree.find('head')
            if head is not None and len(head):
                o = etree.XML(trans.browser_timing_header())
                head.insert(0, o)
            foot = result.tree.find('body')
            if foot is not None and len(foot):
                nr_footer = trans.browser_timing_footer()
                if nr_footer:
                    o = etree.XML(trans.browser_timing_footer())
                    foot.insert(len(foot.getchildren()), o)
            return result