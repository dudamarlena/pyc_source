# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/aws/inlineuserpref/atkssfields.py
# Compiled at: 2009-12-16 03:08:32
"""Overrides rules for KSS inline editing depending on personal preferences"""
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.browserlayer import utils as browserlayer_utils
from archetypes.kss.interfaces import IInlineEditingEnabled
from archetypes.kss.fields import InlineEditingEnabledView as OriginalView
from aws.inlineuserpref.interfaces import IAWSInlineUserPrefLayer

class InlineEditingEnabledView(OriginalView):
    __module__ = __name__
    __doc__ = OriginalView.__doc__
    implements(IInlineEditingEnabled)

    def __call__(self):
        """See base class
        """
        enabled = super(InlineEditingEnabledView, self).__call__()
        if enabled and IAWSInlineUserPrefLayer in browserlayer_utils.registered_layers():
            portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
            member = portal_state.member()
            if member:
                enabled = member.getProperty('enable_inline_editing')
        return enabled