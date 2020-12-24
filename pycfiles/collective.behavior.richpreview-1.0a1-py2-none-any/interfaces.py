# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/interfaces.py
# Compiled at: 2018-04-05 17:11:04
from collective.behavior.richpreview import _
from zope import schema
from zope.interface import Interface

class IBrowserLayer(Interface):
    """A layer specific for this add-on product."""
    pass


class IRichPreviewSettings(Interface):
    """Schema for the control panel form."""
    enable = schema.Bool(title=_('Enable Rich Link Previews?'), description=_(''), default=True)