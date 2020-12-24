# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/canonicalpath/catalog.py
# Compiled at: 2010-06-01 09:56:52
from zope.interface import Interface
from zope.component import queryAdapter
try:
    from plone.indexer.decorator import indexer
    IS_NEW = True
except:
    IS_NEW = False

    class IDummyInterface:
        __module__ = __name__


    class indexer:
        __module__ = __name__

        def __init__(self, *interfaces):
            self.interfaces = (
             IDummyInterface,)

        def __call__(self, callable):
            callable.__component_adapts__ = self.interfaces
            callable.__implemented__ = Interface
            return callable


from interfaces import ICanonicalPath
from interfaces import ICanonicalLink

@indexer(Interface)
def canonical_path(obj, **kwargs):
    """Return canonical_path property for the object.
    """
    adapter = queryAdapter(obj, interface=ICanonicalPath)
    if adapter:
        return adapter.canonical_path
    return


@indexer(Interface)
def canonical_link(obj, **kwargs):
    """Return canonical_link property for the object.
    """
    adapter = queryAdapter(obj, interface=ICanonicalLink)
    if adapter:
        return adapter.canonical_link
    return


if not IS_NEW:
    from Products.CMFPlone.CatalogTool import registerIndexableAttribute
    map(registerIndexableAttribute, ('canonical_path', 'canonical_link'), (
     canonical_path, canonical_link))