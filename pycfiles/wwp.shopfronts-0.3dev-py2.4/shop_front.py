# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/shopfronts/interfaces/shop_front.py
# Compiled at: 2009-09-24 08:20:01
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from wwp.shopfronts import shopfrontsMessageFactory as _

class Ishop_front(Interface):
    """Online shopfronts for stores"""
    __module__ = __name__
    rssfeed = schema.TextLine(title=_('Feed to post'), required=False, description=_('RSS/news feed from twitter, blog, facebook, etc'))
    shopphone = schema.TextLine(title=_('Telephone'), required=False, description=_('enter telephone number'))
    shopwebsite = schema.TextLine(title=_('Website'), required=False, description=_('htt://....'))
    shopaddress = schema.Text(title=_('Address'), required=False, description=_('enter store address'))
    store_logo = schema.Bytes(title=_('Store logo'), required=True, description=_('Upload a logo for the store'))
    store_image = schema.Bytes(title=_('Store Image'), required=True, description=_('Upload an image of the store'))
    special_notices = schema.Text(title=_('Special Notices'), required=True, description=_('Enter details of special offers, or notices'))
    opening_times = schema.Text(title=_('Store opening times'), required=True, description=_('enter the daily opening times of the store'))
    long_desc = schema.SourceText(title=_('Detailed store info'), required=True, description=_('Enter the detailed store information'))