# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/UpfrontContacts/interfaces.py
# Compiled at: 2010-03-10 13:47:45
from zope.interface import Interface

class IPerson(Interface):
    """ Person """
    __module__ = __name__


class IOrganisation(Interface):
    """ Organisation """
    __module__ = __name__