# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/catalog/content/easyshop_image.py
# Compiled at: 2008-09-03 11:14:29
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.image import ATImage
from easyshop.core.interfaces import IEasyShopImage
from easyshop.core.interfaces import IImageConversion
from easyshop.core.config import *
schema = Schema((StringField(name='subtitle', widget=StringWidget(label='Subtitle', label_msgid='schema_subtitle_label', description='A subtitle for the image', description_msgid='schema_subtitle_description', i18n_domain='EasyShop')),))

class EasyShopImage(ATImage):
    """An extended image for EasyShop.
    """
    __module__ = __name__
    implements(IEasyShopImage)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATImage.schema.copy() + schema

    def manage_afterPUT(self, data, marshall_data, file, context, mimetype, filename, REQUEST, RESPONSE):
        """Overwritten to set image.
        """
        file.seek(0)
        self.setImage(file)

    def setImage(self, data, **kwargs):
        """
        """
        if data and data != 'DELETE_IMAGE':
            data = IImageConversion(self).convertImage(data)
        super(EasyShopImage, self).setImage(data)


registerType(EasyShopImage, PROJECTNAME)