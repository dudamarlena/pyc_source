# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/allowsearch/interfaces.py
# Compiled at: 2007-10-24 07:50:42
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 52344 $'
__version__ = '$Revision: 52344 $'[11:-2]
from zope import interface

class IAllowedRolesAndUsers(interface.Interface):
    """ a utility which returns a role / user to allow search for """
    __module__ = __name__

    def __call__(obj, portal, **kwargs):
        """ return a list of allowed roles and users. See the
            CatalogTool.py for more information """
        pass


class IAllowAnonymousSearchMarker(interface.Interface):
    """ a marker interface to mark objects which are
        to be allowed to search for anonymous users """
    __module__ = __name__