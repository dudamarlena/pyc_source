# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/themecustomizer/src/collective/themecustomizer/interfaces.py
# Compiled at: 2014-01-10 10:10:36
from collective.themecustomizer import _
from plone.app.controlpanel.site import ISiteSchema as IBaseSiteSchema
from zope import schema
from zope.interface import Interface

class IThemeCustomizer(Interface):
    """A layer specific for this add-on product.
    """
    pass


class ISiteSchema(IBaseSiteSchema):
    show_header_text = schema.Bool(title=_('Display text in header'), description=_('Displays site title and description on every site page.'), required=False, default=False)
    image = schema.Bytes(title=_('Logo image'), description=_('The image you upload will replace default site logo. Once saved, if you want to get back the original one, just remove your chosen image.'), required=False)
    show_header_logo = schema.Bool(title=_('Display logo in header'), description=_(''), required=False, default=True)
    background = schema.Bytes(title=_('Header background image'), description=_(''), required=False)