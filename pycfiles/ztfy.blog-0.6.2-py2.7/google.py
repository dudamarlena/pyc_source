# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/interfaces/google.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from zope.interface import Interface
from zope.schema import Bool, Int, TextLine, Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from ztfy.blog import _

class IGoogleAnalytics(Interface):
    """Google analytics interface"""
    enabled = Bool(title=_('Activate Google analytics ?'), description=_('Are Google analytics statistics activated ?'), required=True, default=False)
    website_id = TextLine(title=_('Web site ID'), description=_('Google analytics web site ID'), required=False)
    verification_code = TextLine(title=_('Web site verification code'), description=_('Google site verification code'), required=False)


BOTTOM = 0
BOTTOM_TOPICS = 1
TOP = 2
TOP_TOPICS = 3
SLOT_POSITIONS_LABELS = (
 _('Bottom (all pages)'),
 _('Bottom (topics only)'),
 _('Top (all pages)'),
 _('Top (topics only'))
SLOT_POSITIONS = SimpleVocabulary([ SimpleTerm(i, i, t) for i, t in enumerate(SLOT_POSITIONS_LABELS) ])

class IGoogleAdSense(Interface):
    """GoogleAds interface"""
    enabled = Bool(title=_('Activate Google AdSense ?'), description=_('Integrate GoogleAdSense into your web site ?'), required=True, default=False)
    client_id = TextLine(title=_('Client ID'), description=_('Google AdSense client ID'), required=False)
    slot_id = TextLine(title=_('Slot ID'), description=_('ID of the selected slot'), required=False)
    slot_width = Int(title=_('Slot width'), description=_('Width of the selected slot, in pixels'), required=False)
    slot_height = Int(title=_('Slot height'), description=_('Height of the selected slot, in pixels'), required=False)
    slot_position = Choice(title=_('Slot position'), description=_('Position of the selected slot in the generated pages'), vocabulary=SLOT_POSITIONS, default=BOTTOM, required=True)

    def display(context, position):
        """Return boolean value to say if content provider should be displayed"""
        pass