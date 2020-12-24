# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/util.py
# Compiled at: 2009-08-21 14:46:18
"""
$Id: util.py 301 2009-08-21 18:46:18Z falko $
"""
from zope import interface, component
from falkolab.resource.interfaces import IResourceType
from zope.schema.interfaces import IVocabularyFactory
from zope.component.interfaces import ComponentLookupError
from zope.app.component.vocabulary import UtilityVocabulary

class ResourceTypesVocabulary(UtilityVocabulary):
    __module__ = __name__
    interface.classProvides(IVocabularyFactory)
    interface = IResourceType
    nameOnly = True


def _findResourceType(path, allowed=None, default=None):
    """Find first match resourceType by name. Optionally use allowed type names.
    Default resource name used if not find
    """
    if allowed and default and default not in allowed:
        raise ValueError('default resource type name must be in allowed list')
    if allowed:
        reglist = [ (name, component.getUtility(IResourceType, name=name)) for name in allowed ]
    else:
        reglist = component.getUtilitiesFor(IResourceType)
    for (name, resourceType) in reglist:
        if resourceType.matchName(path):
            return resourceType

    resourceType = None
    if default:
        resourceType = component.queryUtility(IResourceType, name=default)
        if resourceType == None:
            raise ComponentLookupError("Can't find resource type '%s'" % default)
    return resourceType