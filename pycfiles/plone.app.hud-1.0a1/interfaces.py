# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/plone.hud/plone.app.hud/src/plone/app/hud/interfaces.py
# Compiled at: 2013-07-28 05:46:55
"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface

class IPloneAppHudLayer(Interface):
    """ A layer specific for this add-on product.

    This interface is referred in browserlayer.xml.

    All views and viewlets register against this layer will appear on
    your Plone site only when the add-on installer has been run.
    """
    pass