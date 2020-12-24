# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/payment/content/direct_debit.py
# Compiled at: 2008-09-03 11:15:14
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes.atapi import *
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType
from Products.ATContentTypes.content.base import ATCTMixin
from easyshop.core.interfaces import IDirectDebitPaymentMethod
from easyshop.core.config import PROJECTNAME
schema = Schema((TextField(name='note', widget=TextAreaWidget(label='Note', description='This text will be displayed on the invoice', label_msgid='schema_note_label', description_msgid='schema_note_description', i18n_domain='EasyShop')), ImageField(name='image', sizes={'large': (768, 768), 'preview': (400, 400), 'mini': (200, 200), 'thumb': (128, 128), 'tile': (64, 64), 'icon': (32, 32), 'listing': (16, 16)}, widget=ImageWidget(label='Image', label_msgid='schema_image_label', i18n_domain='EasyShop'), storage=AttributeStorage())))

class DirectDebitPaymentMethod(OrderedBaseFolder):
    """
    """
    __module__ = __name__
    implements(IDirectDebitPaymentMethod)
    security = ClassSecurityInfo()
    _at_rename_after_creation = True
    schema = ATCTMixin.schema.copy() + schema


registerType(DirectDebitPaymentMethod, PROJECTNAME)