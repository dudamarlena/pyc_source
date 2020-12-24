# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/config.py
# Compiled at: 2008-12-29 10:27:47
__doc__ = 'Common configuration constants\n'
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'collective.roundabout'
ADD_PERMISSIONS = {'RoundAbout Map Hotspot': 'collective.roundabout: Add RoundAbout Map Hotspot', 'RoundAbout Map': 'collective.roundabout: Add RoundAbout Map', 'RoundAbout Image Hotspot': 'collective.roundabout: Add RoundAbout Image Hotspot', 'RoundAbout Image': 'collective.roundabout: Add RoundAbout Image', 'RoundAbout Tour': 'collective.roundabout: Add RoundAbout Tour'}
setDefaultRoles('collective.roundabout: Add RoundAbout Map Hotspot', ('Manager', 'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Map', ('Manager', 'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Image Hotspot', ('Manager',
                                                                        'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Image', ('Manager', 'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Tour', ('Manager', 'Contributer'))