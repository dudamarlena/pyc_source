# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/view.py
# Compiled at: 2010-12-07 02:01:07
from zope.browserresource.resources import Resources
from zope.interface.declarations import implements
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.publisher.interfaces import NotFound
from falkolab.cacheburster.url import _name_map

class VersionedResources(Resources):
    implements(IBrowserPublisher)

    def publishTraverse(self, request, name):
        try:
            resource = super(VersionedResources, self).publishTraverse(request, name)
            tStak = request.getTraversalStack()
            request.setTraversalStack([ _name_map.get(name, name) for name in tStak ])
        except NotFound:
            orig_name = _name_map.get(name)
            if orig_name is None:
                raise NotFound(self, name)
            resource = super(VersionedResources, self).publishTraverse(request, orig_name)

        return resource