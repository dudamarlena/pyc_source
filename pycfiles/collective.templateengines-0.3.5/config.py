# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/config.py
# Compiled at: 2013-03-13 08:34:51
PROJECTNAME = 'collective.teaser'
DEFAULT_IMPORTANCE = ('3', )
ADD_PERMISSIONS = {'Teaser': 'collective.teaser: Add Teaser'}
from Products.CMFCore.permissions import setDefaultRoles
DEFAULT_ADD_CONTENT_PERMISSION = 'Add portal content'
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner', 'Contributor'))