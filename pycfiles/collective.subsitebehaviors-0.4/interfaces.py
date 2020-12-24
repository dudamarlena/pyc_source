# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/interfaces.py
# Compiled at: 2015-02-05 14:49:09
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ICollectiveSubsiteBehaviorsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    pass


class ISubsiteLogo(Interface):
    """"""
    pass