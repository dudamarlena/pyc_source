# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eleddy/buildouts/umich/src/collective.purge_behaviors/collective/purge_behaviors/interfaces.py
# Compiled at: 2013-07-01 23:09:36
from zope.interface import Interface

class IPurgeParent(Interface):
    """ Marker interface for purging an items parent
    """
    pass


class IPurgeSiblings(Interface):
    """ Marker interface for purging an items siblings
    """
    pass


class IPurgeContents(Interface):
    """ Marker interface for purging a containers contents
    """
    pass


class IPurgeSite(Interface):
    """ Marker interface for purging the home page
    """
    pass