# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/widget/attachments.py
# Compiled at: 2009-04-26 22:17:24
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

class AttachmentsManagerWidget(TypesWidget):
    """This widget adds support for uploading attachments into documents. To 
    support this, you must use it on a folderish type (derived from BaseFolder) 
    with 'FileAttachment' in the allowed_content_types. Create a BooleanField 
    and use this widget. This will display a form at the bottom of your edit 
    form (presuming it's the last widget, which it probably ought to be) where 
    you can upload images into your content type. The boolean field itself is
    used to select whether an attachment download box should be presented. This
    is similar to the "related items" box in Plone.
    
    Content editors may also reference the images directly in their body
    text.
    
    Caveats: In the edit macro, the upload button may steal the default 
    enter-key-press in base_edit.
    """
    __module__ = __name__
    _properties = TypesWidget._properties.copy()
    _properties.update({'macro': 'widget_attachmentsmanager', 'expanded': False})


registerWidget(AttachmentsManagerWidget, title='Attachments manager widget', description=('Renders controls for uploading attachments to documents', ), used_for=('Products.Archetypes.Field.BooleanField', ))