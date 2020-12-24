# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ifrit/adapters.py
# Compiled at: 2007-02-17 17:57:25
""" ifrist adapters

$Id: adapters.py,v 1.8 2007/02/17 22:57:25 tseaver Exp $
"""
from StringIO import StringIO
from zope.component import getUtility
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.interface import directlyProvides
from zope.interface import Provides
from zope.interface.declarations import getObjectSpecification
from zope.location import LocationProxy
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
from ifrit.interfaces import IElement
from ifrit.interfaces import IElementFactory
from ifrit.interfaces import IStreamParser
from ifrit.interfaces import IXMLSerialization

class OFSFileAsXML(object):
    """ "Convert" OFS.Image.File-like object to XML.

    o Assume that the 'data' element is a string, unicode, or a pdata chunk,
      containing the actual XML to be returned.
    """
    __module__ = __name__
    implements(IXMLSerialization)

    def __init__(self, context):
        self.context = context

    def serialize(self, buffer):
        data = self.context.data
        if isinstance(data, str):
            buffer.write(data)
        else:
            if isinstance(data, unicode):
                buffer.write(data.encode('utf8'))
            while data is not None:
                buffer.write(data.data)
                data = data.next

        return


class ElementMaker(object):
    """ Adapter factories which use paths to find nodes.
    """
    __module__ = __name__
    implements(IElementFactory)

    def __init__(self, path=None, parser_name=None, multiple=False):
        self.path = path
        self.parser_name = parser_name or 'elementtree'
        self.multiple = multiple

    def __call__(self, context):
        buffer = StringIO()
        adapter = IXMLSerialization(context)
        adapter.serialize(buffer)
        buffer.seek(0)
        parser = getUtility(IStreamParser, name=self.parser_name)
        tree = parser(buffer).getroot()
        if self.multiple:
            if self.path is not None:
                nodes = tree.findall(self.path)
            else:
                nodes = [
                 tree.getroot()]
            return nodes
        else:
            if self.path is not None:
                node = tree.find(self.path)
            else:
                node = tree
            return node
        return


class _ProvidedByDescriptor(object):
    __module__ = __name__

    def __get__(self, inst, cls=None):
        if inst is None:
            return getObjectSpecification(cls)
        else:
            return getObjectSpecification(inst)
        return

    def __set__(self, inst, value):
        raise TypeError("Can't set __providedBy__ on a decorated object")


class _ElementProxy(LocationProxy):
    __module__ = __name__
    __slots__ = ('__name__', '__parent__', '__provides__')
    __providedBy__ = _ProvidedByDescriptor()

    def __init__(self, ob, container=None, name=None, *provides):
        super(_ElementProxy, self).__init__(ob, container, name)
        self.__provides__ = Provides(provides)


class ElementTraversalAdapter(object):
    __module__ = __name__
    implements(IPublishTraverse)

    def __init__(self, context, markers=None, proxy_class=_ElementProxy):
        if markers is None:
            markers = {}
        self.context = context
        self.markers = markers
        self.proxy_class = proxy_class
        return

    def publishTraverse(self, request, name):
        """ See IPublishTraverse.
        """
        element = queryAdapter(self.context, IElement, name)
        if element is None:
            view = queryMultiAdapter((self.context, request), name=name)
            if view is not None:
                return view
            raise NotFound(self.context, name, request)
        proxy = self.proxy_class(element, container=self.context, name=name)
        marker = self.markers.get(name)
        if marker is not None:
            directlyProvides(proxy, marker)
        of = getattr(proxy, '__of__', None)
        if of is not None:
            proxy = of(self.context)
        return proxy


_PROXIES_WITH_BASES = {(): _ElementProxy}

class ElementTraversalAdapterFactory(object):
    __module__ = __name__

    def __init__(self, markers, bases=()):
        self.markers = markers
        self.bases = tuple(bases)

    def __call__(self, context, request=None):
        klass = _PROXIES_WITH_BASES.get(self.bases)
        if klass is None:
            bases = (
             _ElementProxy,) + self.bases
            name = ('_').join([ x.__name__ for x in bases ])
            klass = type(_ElementProxy)(name, bases, {})
            _PROXIES_WITH_BASES[bases] = klass
        return ElementTraversalAdapter(context, self.markers, klass)