# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/interfaces.py
# Compiled at: 2013-03-13 08:34:51
from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager

class ITeaser(Interface):
    """Marker interface.
    """
    pass


class ITeaserLayer(Interface):
    """Browser Layer for teaser.
    """
    pass


class ITeaserPortletManager(IPortletManager):
    """Teaser Portlet Manager
    """
    pass