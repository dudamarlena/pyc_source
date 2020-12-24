# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/indexing.py
# Compiled at: 2007-10-12 18:11:48
from Acquisition import aq_inner
from lovely.tag import interfaces
from zope.component.interfaces import ComponentLookupError
from Products.CMFPlone.CatalogTool import registerIndexableAttribute

def tags(object, portal, **kwargs):
    """Return the list of tags for a particular object.
    """
    try:
        tagging = interfaces.ITagging(aq_inner(object), None)
        if tagging is None:
            raise AttributeError('Could not look up ITagging adapter')
        return list(tagging.getTags())
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError

    return


registerIndexableAttribute('tags', tags)