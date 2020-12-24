# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/croppingimage/schema.py
# Compiled at: 2008-07-23 09:49:01
from Products.Archetypes.public import BaseSchema, Schema
from Products.Archetypes.public import ImageField
from Products.Archetypes.public import ImageWidget
from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.validation import V_REQUIRED
from field import CroppingImageField
cropping_image_schema = BaseSchema + Schema((CroppingImageField('image', required=True, primary=True, languageIndependent=True, long_edge_size=600, short_edge_size=450, sizes={'large': (600, 450), 'medium': (300, 225), 'thumb': (125, 94)}, validators=(('isNonEmptyFile', V_REQUIRED), ('checkImageMaxSize', V_REQUIRED)), widget=ImageWidget(description='', label='Image', label_msgid='label_image', i18n_domain='plone', show_content_type=False)),), marshall=PrimaryFieldMarshaller())