# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/interfaces.py
# Compiled at: 2014-11-07 05:17:11
"""Module where all interfaces, events and exceptions live."""
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.contact.membrane import _

class ICollectiveContactMembraneLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    pass


class IContactMembraneParameters(Interface):
    """Parameters for collective.contact.membrane product."""
    active_held_position_states = schema.List(title=_('Active states for held positions'), description=_('States of the held positions for which the person is member of the group.'), required=False)