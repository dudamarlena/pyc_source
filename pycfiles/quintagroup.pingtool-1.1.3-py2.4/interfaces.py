# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/interfaces.py
# Compiled at: 2009-03-31 04:47:33
from zope.interface import Interface

class IPingTool(Interface):
    """ Interface for PingTool.
    """
    __module__ = __name__


class ICanonicalURL(Interface):
    """ Interface for canonical URL API providing."""
    __module__ = __name__

    def getCanonicalURL():
        """Get canonical_url property value."""
        pass


class ISyndicationObject(Interface):
    """ Interface for Syndicaion providing."""
    __module__ = __name__