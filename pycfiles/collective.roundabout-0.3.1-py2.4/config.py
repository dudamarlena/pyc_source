# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/config.py
# Compiled at: 2008-12-29 10:27:47
"""Common configuration constants
"""
from Products.CMFCore.permissions import setDefaultRoles
PROJECTNAME = 'collective.roundabout'
ADD_PERMISSIONS = {'RoundAbout Map Hotspot': 'collective.roundabout: Add RoundAbout Map Hotspot', 'RoundAbout Map': 'collective.roundabout: Add RoundAbout Map', 'RoundAbout Image Hotspot': 'collective.roundabout: Add RoundAbout Image Hotspot', 'RoundAbout Image': 'collective.roundabout: Add RoundAbout Image', 'RoundAbout Tour': 'collective.roundabout: Add RoundAbout Tour'}
setDefaultRoles('collective.roundabout: Add RoundAbout Map Hotspot', ('Manager', 'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Map', ('Manager', 'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Image Hotspot', ('Manager',
                                                                        'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Image', ('Manager', 'Contributer'))
setDefaultRoles('collective.roundabout: Add RoundAbout Tour', ('Manager', 'Contributer'))