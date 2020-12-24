# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowsearch/adapters.py
# Compiled at: 2008-03-13 07:09:46
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 60620 $'
__version__ = '$Revision: 60620 $'[11:-2]
from zope import component
from zope import interface
from collective.allowsearch.interfaces import IAllowedRolesAndUsers
from collective.allowsearch.interfaces import IAllowAnonymousSearchMarker

class AllowAnonSearch(object):
    """ adapter to which checks for an interface on its context
        to determine if 'Anonymous' users are to view catalog
        brains for the given object. """
    __module__ = __name__
    interface.implements(IAllowedRolesAndUsers)
    ROLE = 'Anonymous'

    def __init__(self, context):
        self.context = context

    def __call__(self, obj, portal, **kw):
        allowed = component.getUtility(IAllowedRolesAndUsers, 'collective.allowsearch.default')(obj, portal, **kw)
        if IAllowAnonymousSearchMarker.providedBy(obj):
            if self.ROLE not in allowed:
                allowed.append(self.ROLE)
        return allowed