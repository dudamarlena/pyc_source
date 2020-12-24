# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/misc.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class ICompleteness(Interface):
    """Provides methods to check completeness.
    """
    __module__ = __name__

    def isComplete():
        """Checks whether the data of an object is complete.
        """
        pass


class IType(Interface):
    """Provides methods to get type informations.
    """
    __module__ = __name__

    def getType():
        """Returns the type of the object.
        """
        pass


class IValidity(Interface):
    """Provides methods to check validity.
    """
    __module__ = __name__

    def isValid(**kwargs):
        """Returns true if the object fullfills criteria of validity.
        """
        pass


class IMailAddresses(Interface):
    """Provides methods to retrieve mail addresses.
    """
    __module__ = __name__

    def getSender():
        """Returns the sender of shop e-mails based on the entered data.
        """
        pass

    def getReceivers():
        """Returns receivers of shop e-mails based on entered data.
        """
        pass