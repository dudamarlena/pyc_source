# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/examples/FSSItem.py
# Compiled at: 2008-10-23 05:55:17
"""
Demo content type with a file and an image.
$Id: FSSItem.py 65108 2008-05-19 20:23:31Z cbosse $
"""
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import FileField
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import TextField
from Products.Archetypes.public import FileWidget
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.public import TextAreaWidget
from Products.Archetypes.public import PrimaryFieldMarshaller
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.base import ATContentTypeSchema
from iw.fss.config import PROJECTNAME
from iw.fss.FileSystemStorage import FileSystemStorage
BaseItemShema = Schema((FileField('file', required=False, primary=True, storage=FileSystemStorage(), widget=FileWidget(description="Select the file to be added by clicking the 'Browse' button.", description_msgid='help_file', label='File', label_msgid='label_file', i18n_domain='plone', show_content_type=False)), ImageField('image', required=False, sizes={'mini': (40, 40), 'thumb': (80, 80)}, storage=FileSystemStorage(), widget=ImageWidget()), TextField('text', required=False, storage=FileSystemStorage(), widget=TextAreaWidget())), marshall=PrimaryFieldMarshaller())
FSSItemSchema = BaseSchema.copy() + BaseItemShema.copy()
ATFSSItemSchema = ATContentTypeSchema.copy() + BaseItemShema.copy()

class FSSItem(BaseContent):
    """A simple item using FileSystemStorage"""
    __module__ = __name__
    archetypes_name = portal_type = meta_type = 'FSSItem'
    schema = FSSItemSchema
    _at_rename_after_creation = True


registerType(FSSItem, PROJECTNAME)

class ATFSSItem(ATCTContent):
    """A simple item using FileSystemStorage base on ATContentypes"""
    __module__ = __name__
    archetypes_name = portal_type = meta_type = 'ATFSSItem'
    schema = ATFSSItemSchema
    _at_rename_after_creation = True


registerType(ATFSSItem, PROJECTNAME)