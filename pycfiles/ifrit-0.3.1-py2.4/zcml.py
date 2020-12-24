# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ifrit/zcml.py
# Compiled at: 2007-02-17 17:57:25
""" ifrit ZCML directives

$Id: zcml.py,v 1.7 2007/02/17 22:57:25 tseaver Exp $
"""
from zope.component import provideAdapter
from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import GlobalObject
from zope.configuration.fields import Path
from zope.configuration.fields import PythonIdentifier
from zope.configuration.fields import Tokens
from zope.configuration.fields import Bool
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import IRequest
from ifrit.interfaces import IElement
from ifrit.adapters import ElementMaker
from ifrit.adapters import ElementTraversalAdapterFactory

class IPathAdapter(Interface):
    """ Interface for directive which creates a path-based adapter.

    E.g.:

     <ifrit:path_adapter
       for="package.interfaces.IContent"
       name="adapterName"
       path="some_lxml_path"
       parser_name="objectify"
       module="package.module"
       factory_name="factoryName"
       />

    o Create an adapter factory which uses 'path' to extract a node
      from the serialized XML, as parsed by the utility identifed
      by 'parser_name'.

    o Bind that factory into 'module' under 'factory_name'.

    o Register that factory as providing an 'IElement' adapter for
      the 'for' interface, using the 'name' if provided (otherwise,
      registers it as the default adapter).
    """
    __module__ = __name__
    module = GlobalObject(title='Target module', description='Module into which the generated adapter factory will be added.', required=True)
    factory_name = PythonIdentifier(title='Factory name', description='Name of the generated adapter factory.', required=True)
    path = TextLine(title='Path', description='XPath or ElementTree path expression', required=True)
    parser_name = PythonIdentifier(title='Parser name', description='Name of IStreamParser utility used to parse XML', required=False, default='elementtree')
    for_ = Tokens(title='Specifications to be adapted', description='This should be a list of interfaces or classes', value_type=GlobalObject(missing_value=object()), required=False)
    name = PythonIdentifier(title='Adapter name', description='Name under which the adapter is registered.', required=False)
    multiple = Bool(title='Multiple', description='Does the factory return a sequence?', required=False, default=False)


def createPathAdapter(module, factory_name, path, parser_name, for_, name, multiple):
    """ Create an adapter factory using 'path'.
 
    o Seat the new schema into 'module' under 'factory_name'.
    """
    factory = ElementMaker(path, parser_name, multiple)
    setattr(module, factory_name, factory)
    provideAdapter(factory, for_, IElement, name)


def PathAdapterDirective(_context, module, factory_name, path, parser_name='elementtree', for_=None, name='', multiple=False):
    _context.action(discriminator=(module, factory_name), callable=createPathAdapter, args=(module, factory_name, path, parser_name, for_, name, multiple))


class ITraversalAdapter(Interface):
    """ Interface for directive which creates a traveral adapter factory.

    E.g.:

     <ifrit:traversal_adapter
        for="ifrit.tests.IDummy"
        module="ifrit.tests"
        factory_name="traversalFactory">
      <ifrit:marker
        name="items"
        interface="ifrit.tests.IMarker"
     </ifrit:traversal_adapter>

    o Create a traversal adapter factory, which stamps the returned node
      with the marker interface passed in the corresponding 'marker'.

    o Bind that factory into 'module' under 'factory_name'.

    o Register that factory as providing the default 'IPathTraverser' adapter
      for the 'for' interface.
    """
    __module__ = __name__
    module = GlobalObject(title='Target module', description='Module into which the generated adapter factory will be added.', required=True)
    factory_name = PythonIdentifier(title='Factory name', description='Name of the generated traversal adapter factory.', required=True)
    for_ = Tokens(title='Specifications to be adapted', description='This should be a list of interfaces or classes', value_type=GlobalObject(missing_value=object()), required=False)
    bases = Tokens(title='Classes to be added as bases of adapters', description='This should be a list of classes', value_type=GlobalObject(missing_value=object()), required=False)


class ITraversalMarkerDirective(Interface):
    """ Sub-directive schema for <ifrit:marker>.
    """
    __module__ = __name__
    name = PythonIdentifier(title='Traversal name', description='Name traversed by the adapter.', required=True)
    interface = GlobalInterface(title='Merker Interface', description='Interface to be stamped onto returned nodes', required=False)


def createTraversalAdapter(module, factory_name, for_, markers, bases):
    """ Create an adapter factory using 'path'.
 
    o Seat the new schema into 'module' under 'factory_name'.
    """
    factory = ElementTraversalAdapterFactory(markers, bases)
    setattr(module, factory_name, factory)
    provideAdapter(factory, for_, IPublishTraverse)
    provideAdapter(factory, for_ + (IRequest,), IPublishTraverse)


class TraversalAdapterDirective(object):
    __module__ = __name__

    def __init__(self, _context, module, factory_name, for_=None, bases=()):
        self._context = _context
        self.module = module
        self.factory_name = factory_name
        self.for_ = for_
        self.bases = tuple(bases)
        self._markers = {}

    def marker(self, context, name, interface):
        self._markers[name] = interface

    def __call__(self):
        for_ = tuple(self.for_)
        self._context.action(discriminator=('adapter', for_, IPublishTraverse, ''), callable=createTraversalAdapter, args=(self.module, self.factory_name, for_, self._markers, self.bases))