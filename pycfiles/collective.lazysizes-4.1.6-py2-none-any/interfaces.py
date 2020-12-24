# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/interfaces.py
# Compiled at: 2018-09-10 10:58:04
from collective.lazysizes import _
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from zope.interface import Interface

class ILazySizesLayer(Interface):
    """A layer specific for this add-on product."""
    pass


class ILazySizesSettings(model.Schema):
    """Schema for the control panel form."""
    lazyload_authenticated = schema.Bool(title=_('title_lazyload_authenticated', default='Enable for authenticated users?'), description=_('description_lazyload_authenticated', default='By default, images and iframes are lazy loaded only for anonymous users. If selected, lazy loading will be enabled for all users.'), default=False)
    form.widget('css_class_blacklist', cols=25, rows=10)
    css_class_blacklist = schema.Set(title=_('title_css_class_blacklist', default='CSS class blacklist'), description=_('description_css_class_blacklist', default='A list of CSS class identifiers that will not be processed for lazy loading. &lt;img&gt; and &lt;iframe&gt; elements with that class directly applied to them, or to a parent element, will be skipped.'), required=False, default=set(), value_type=schema.ASCIILine(title=_('title_css_class_blacklist_value_type', default='CSS class')))