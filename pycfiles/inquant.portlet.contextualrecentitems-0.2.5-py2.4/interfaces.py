# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/portlet/contextualrecentitems/interfaces.py
# Compiled at: 2008-02-18 06:13:46
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 58891 $'
__version__ = '$Revision: 58891 $'[11:-2]
from zope import interface

class ITypeNameProvider(interface.Interface):
    """ a thing which is able to proveide us with a name of a
        portal type """
    __module__ = __name__
    type = interface.Attribute('the type name')