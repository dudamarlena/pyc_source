# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Applications/Plone/zinstance/src/collective.volunteer/collective/volunteer/content/volunteerday.py
# Compiled at: 2008-11-10 22:01:30
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.validation import V_REQUIRED
from Products.ATContentTypes.configuration import zconf
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from collective.volunteer.config import *
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.lib.imagetransform import ATCTImageTransform
from collective.volunteer.validators import isVolunteerSlotLine
copied_fields = {}
copied_fields['title'] = BaseSchema['title'].copy()
copied_fields['title'].searchable = True
schema = Schema((copied_fields['title'], DateTimeField(name='date', widget=DateTimeField._properties['widget'](label='Date of volunteering', show_hm=False), required=True), LinesField(name='timesAvailable', required=True, widget=LinesWidget(label='Times Available', description='The format is "time|description|user id". User id is not required since it will be filled in when users select the times.  Ex. "10:00am-11:00am|Front Desk" '), validators=(isVolunteerSlotLine(),))))
VolunteerDaySchema = BaseSchema.copy() + schema.copy()

class VolunteerDay(BaseContent, BrowserDefaultMixin):
    """
    
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    implements(interfaces.IVolunteerDay)
    meta_type = 'VolunteerDay'
    portal_type = 'VolunteerDay'
    _at_rename_after_creation = True
    schema = VolunteerDaySchema


registerType(VolunteerDay, PRODUCT_NAME)