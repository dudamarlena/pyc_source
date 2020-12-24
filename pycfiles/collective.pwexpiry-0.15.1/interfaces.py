# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eleddy/buildouts/umich/src/collective.purge_behaviors/collective/purge_behaviors/interfaces.py
# Compiled at: 2013-07-01 23:09:36
from zope.interface import Interface

class IPurgeParent(Interface):
    """ Marker interface for purging an items parent
    """


class IPurgeSiblings(Interface):
    """ Marker interface for purging an items siblings
    """


class IPurgeContents(Interface):
    """ Marker interface for purging a containers contents
    """


class IPurgeSite(Interface):
    """ Marker interface for purging the home page
    """