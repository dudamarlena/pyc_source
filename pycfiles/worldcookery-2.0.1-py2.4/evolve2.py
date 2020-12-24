# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/generations/evolve2.py
# Compiled at: 2006-09-21 05:27:36
from zope.component.interfaces import ObjectEvent
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
from worldcookery.interfaces import IWorldCookerySite
from worldcookery.session import setUpClientIdAndSessionDataContainer

def evolve(context):
    """Setup client ID manager and session data container."""
    root = getRootFolder(context)
    for site in findObjectsProviding(root, IWorldCookerySite):
        sm = site.getSiteManager()
        if 'session_data' not in sm:
            setUpClientIdAndSessionDataContainer(ObjectEvent(site))