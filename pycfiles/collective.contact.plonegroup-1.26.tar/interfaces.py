# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cedricmessiant/workspace/buildouts/webpro/src/collective.contact.membrane/src/collective/contact/membrane/interfaces.py
# Compiled at: 2014-11-07 05:17:11
__doc__ = 'Module where all interfaces, events and exceptions live.'
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from collective.contact.membrane import _

class ICollectiveContactMembraneLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IContactMembraneParameters(Interface):
    """Parameters for collective.contact.membrane product."""
    active_held_position_states = schema.List(title=_('Active states for held positions'), description=_('States of the held positions for which the person is member of the group.'), required=False)