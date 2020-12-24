# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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