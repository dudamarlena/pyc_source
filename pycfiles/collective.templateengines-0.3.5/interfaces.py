# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/interfaces.py
# Compiled at: 2013-03-13 08:34:51
from zope.interface import Interface
from plone.portlets.interfaces import IPortletManager

class ITeaser(Interface):
    """Marker interface.
    """


class ITeaserLayer(Interface):
    """Browser Layer for teaser.
    """


class ITeaserPortletManager(IPortletManager):
    """Teaser Portlet Manager
    """