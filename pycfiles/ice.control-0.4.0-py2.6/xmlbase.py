# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/controls/tree/xmlbase.py
# Compiled at: 2010-08-27 06:32:04
from zope.interface import implements, Interface
from zope.component import adapts, queryMultiAdapter
from zope.dublincore.interfaces import IZopeDublinCore
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.interface.common.mapping import IEnumerableMapping
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.container.interfaces import IReadContainer
from zope.location.interfaces import ILocationInfo
from zope.security.interfaces import Unauthorized
from zope.size.interfaces import ISized
from interfaces import IXML, ICONS, XMLDOC, XMLNODE, ACCESS_DENIED

class XMLBase(object):
    implements(IXML)
    adapts(Interface, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def name(self):
        try:
            return ILocationInfo(self.context).getName()
        except TypeError:
            return ''

    def path(self):
        return absoluteURL(self.context, self.request) or ''

    def title(self):
        try:
            title = IZopeDublinCore(self.context).title
            if title:
                return '[ ' + title + ' ]'
        except TypeError:
            pass

        return ''

    def icon_url(self):
        icon = queryMultiAdapter((self.context, self.request), name=ICONS)
        if icon:
            return icon.url()
        return ''

    def is_container(self):
        return IReadContainer.providedBy(self.context) or ''

    def size(self):
        try:
            return ISized(self.context).sizeForDisplay()
        except TypeError:
            return ''

    def length(self):
        try:
            enumerable = IEnumerableMapping(self.context)
        except TypeError:
            return ''

        return len(enumerable)

    def sort_key(self):
        return

    def to_xml(self):
        try:
            name = self.name()
        except Unauthorized:
            name = ACCESS_DENIED

        try:
            path = self.path() + '/'
        except Unauthorized:
            path = ACCESS_DENIED

        try:
            title = self.title()
        except Unauthorized:
            title = ACCESS_DENIED

        try:
            icon_url = self.icon_url()
        except Unauthorized:
            icon_url = ACCESS_DENIED

        try:
            size = self.size()
        except Unauthorized:
            size = ACCESS_DENIED

        try:
            length = self.length()
        except Unauthorized:
            length = ACCESS_DENIED

        try:
            is_container = self.is_container() and 'true' or 'false'
        except Unauthorized:
            is_container = ACCESS_DENIED

        return XMLNODE % (name, path, title, icon_url, size,
         length, is_container)

    def node_xmldoc(self):
        return XMLDOC % self.to_xml()

    def children_xmldoc(self):
        try:
            rc = IReadContainer(self.context)
        except TypeError:
            return XMLDOC % ''
        except Unauthorized:
            return XMLDOC % ''

        specs = [ queryMultiAdapter((value, self.request), IXML) for value in rc.values()
                ]
        specs = filter(lambda x: x, specs)
        specs.sort(key=lambda x: x.sort_key())
        nodes = [ x.to_xml() for x in specs ]
        return XMLDOC % ('\n').join(nodes)