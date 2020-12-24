# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/interfaces.py
# Compiled at: 2015-02-05 14:49:09
__doc__ = 'Module where all interfaces, events and exceptions live.'
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ICollectiveSubsiteBehaviorsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ISubsiteLogo(Interface):
    """"""