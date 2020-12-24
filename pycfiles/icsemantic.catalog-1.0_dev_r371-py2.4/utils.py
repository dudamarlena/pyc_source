# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/indexes/utils.py
# Compiled at: 2008-10-06 10:31:12
"""A few common pieces of code used in the catalog indexes in this
package are grouped into functions in this module to make its reuse
easier.
"""
from BTrees.IIBTree import IITreeSet, IISet, intersection, union
from Products.CMFCore.utils import getToolByName
from icsemantic.thesaurus.Thesaurus import thesaurus_utility

def get_equivalent(portal, k, lang=None):
    """Query the local thesaurus for equivalent concepts"""
    try:
        r = thesaurus_utility().get_equivalent(k, lang, exclude=False)
    except IndexError:
        r = []

    return r


def get_related(portal, k, lang=None, contexts=None):
    """Query the local thesaurus for related concepts"""
    try:
        r = thesaurus_utility().get_related(k, lang, exclude=False, contexts=contexts)
    except IndexError:
        r = []

    return r


def build_catalog_results(id, catalog, catalog_results):
    """Build a catalog result simulate an internal catalog result"""
    paths = [ i.getPath() for i in catalog_results ]
    results = []
    for p in paths:
        rid = catalog.hasuid(p)
        if rid is not None:
            results.append(rid)

    return (
     IISet(tuple(results)), (id,))