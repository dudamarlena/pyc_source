# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/config.py
# Compiled at: 2013-03-13 08:34:51
PROJECTNAME = 'collective.teaser'
DEFAULT_IMPORTANCE = ('3', )
ADD_PERMISSIONS = {'Teaser': 'collective.teaser: Add Teaser'}
from Products.CMFCore.permissions import setDefaultRoles
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))