# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowsearch/utilities.py
# Compiled at: 2007-10-24 07:50:42
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 52344 $'
__version__ = '$Revision: 52344 $'[11:-2]
from zope import interface
from collective.allowsearch.interfaces import IAllowedRolesAndUsers
from Products.CMFPlone.CatalogTool import allowedRolesAndUsers

class DefaultAllowedRolesAndUsers(object):
    __module__ = __name__
    interface.implements(IAllowedRolesAndUsers)

    def __call__(self, obj, portal, **kwargs):
        return allowedRolesAndUsers(obj, portal, **kwargs)


default_allowed_roles_and_users = DefaultAllowedRolesAndUsers()