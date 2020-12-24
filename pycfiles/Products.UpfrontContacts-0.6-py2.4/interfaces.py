# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/interfaces.py
# Compiled at: 2010-03-10 13:47:45
from zope.interface import Interface

class IPerson(Interface):
    """ Person """
    __module__ = __name__


class IOrganisation(Interface):
    """ Organisation """
    __module__ = __name__