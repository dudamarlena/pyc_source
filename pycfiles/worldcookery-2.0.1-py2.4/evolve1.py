# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/generations/evolve1.py
# Compiled at: 2006-09-21 05:27:36
from zope.component.interfaces import ObjectEvent
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from zope.app.intid import addIntIdSubscriber
from zope.app.catalog.catalog import indexDocSubscriber
from zope.app.component.site import setSite
from worldcookery.interfaces import IRecipe, IWorldCookerySite
from worldcookery.search import setupCatalogAndIndices

def evolve(context):
    """Setup catalog and indices for fulltext search."""
    root = getRootFolder(context)
    for site in findObjectsProviding(root, IWorldCookerySite):
        sm = site.getSiteManager()
        if 'catalog' not in sm:
            setupCatalogAndIndices(ObjectEvent(site))
            setSite(site)
            for recipe in findObjectsProviding(site, IRecipe):
                addIntIdSubscriber(recipe, ObjectEvent(recipe))
                indexDocSubscriber(ObjectEvent(recipe))

            setSite(None)

    return