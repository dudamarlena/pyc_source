# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/interfaces.py
# Compiled at: 2018-04-05 17:11:04
from collective.behavior.richpreview import _
from zope import schema
from zope.interface import Interface

class IBrowserLayer(Interface):
    """A layer specific for this add-on product."""


class IRichPreviewSettings(Interface):
    """Schema for the control panel form."""
    enable = schema.Bool(title=_('Enable Rich Link Previews?'), description=_(''), default=True)