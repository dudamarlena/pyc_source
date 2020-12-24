# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\content\skinschema.py
# Compiled at: 2010-04-08 08:46:19
from Products.Archetypes.public import *
from aws.minisite.config import I18N_DOMAIN
from Products.SmartColorWidget.Widget import SmartColorWidget
from collective.phantasy.atphantasy.content.skin import PhantasySkinSchema
from aws.minisite import minisiteMessageFactory as _
invisibleShematas = [
 'borders', 'plone-overloads']
invisibleFields = [
 'contentBackgroundImageName']
visibleFields = []
MiniSiteSkinFieldsSchema = Schema((StringField('headerBackgroundImageName', schemata='images', widget=StringWidget(description=_('description_header_background_image_name', 'Enter the header background image name, upload the image in this skin'), label=_('label_header_background_image_name', 'Header Background Image Name'))),
 BooleanField('displayRoundedCorners', schemata='images', default=False, widget=BooleanWidget(description=_('description_display_rounded_corners', 'Do you want to display rounded corners around content ? (use it only for a portal width fixed to 996px, otherwise you may need to overload corner images and styles)'), label=_('label_display_rounded_corners', 'Display Rounded Corners ?'))),
 StringField('portalPadding', schemata='dimensions', widget=StringWidget(label=_('label_portal_padding', 'Portal Padding'), description=_('description_portal_padding', 'Enter the portal padding, ex 10px or 1em ...')))), marshall=RFC822Marshaller())

def finalizeMiniSiteSkinSchema():
    """Finalizes schema to alter some fields
    """
    schema = PhantasySkinSchema.copy()
    for fieldName in schema.keys():
        if fieldName not in visibleFields and schema[fieldName].schemata in invisibleShematas:
            schema[fieldName].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
        elif fieldName in invisibleFields:
            schema[fieldName].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
        elif fieldName == 'footerViewlet':
            schema[fieldName].widget.fck_area_css_class = 'documentContent'
        elif fieldName == 'logoViewlet':
            schema[fieldName].widget.fck_area_css_id = 'portal-header'

    new_schema = schema.copy() + MiniSiteSkinFieldsSchema
    return new_schema


MiniSiteSkinSchema = finalizeMiniSiteSkinSchema()