# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/collective/contentrules/mailadapter/interfaces.py
# Compiled at: 2009-06-10 07:32:58
from zope.interface import Interface

class IRecipientsResolver(Interface):
    """ An adapter for recipient resolving 
        
        Create your own adapter implementing this interface
    """
    __module__ = __name__

    def recipients():
        """ Returns list of emails the mail is send to """
        pass