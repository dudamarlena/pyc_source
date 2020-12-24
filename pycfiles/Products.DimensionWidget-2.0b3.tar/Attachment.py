# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/content/Attachment.py
# Compiled at: 2009-04-26 22:17:24
__author__ = 'Emanuel Sartor <emanuel@menttes.com>, Santiago Bruno <unknown>'
__docformat__ = 'plaintext'
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.DigestoContentTypes.config import *
from iw.fss.FileSystemStorage import FileSystemStorage
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent, IObjectEditedEvent
from zope.app.event.interfaces import IObjectModifiedEvent, IObjectCreatedEvent
from Acquisition import aq_inner, aq_parent
from zope.app.component.interfaces import ISite
schema = Schema((FileField(name='file', widget=FileField._properties['widget'](label='File', label_msgid='DigestoContentTypes_label_file', i18n_domain='DigestoContentTypes'), storage=FileSystemStorage(), searchable=1),))
Attachment_schema = BaseSchema.copy() + schema.copy()

class Attachment(BaseContent, BrowserDefaultMixin):
    """
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    implements(interfaces.IAttachment)
    meta_type = 'Attachment'
    _at_rename_after_creation = True
    schema = Attachment_schema


registerType(Attachment, PROJECTNAME)

@adapter(interfaces.IAttachment, IObjectModifiedEvent)
def handle_attachment_added(obj, event):
    """Handle the IObjectInitializedEvent event for attachments.
    """
    obj.schema['file'].setFilename(obj, obj.id)