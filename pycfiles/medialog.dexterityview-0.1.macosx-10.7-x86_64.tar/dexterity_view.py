# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/Python-2.7/lib/python2.7/site-packages/medialog/dexterityview/dexterity_view.py
# Compiled at: 2015-07-06 11:49:12
from zope.interface import implements, Interface, Attribute
from Products.Five import BrowserView
from plone.dexterity.utils import iterSchemata
from zope.schema import getFields
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.browser.view import DefaultView
from plone import api
from medialog.dexterityview.interfaces import IDexterityViewSettings

class IDexterityView(Interface):
    """
    view interface
    """

    def block_fields():
        """ Returns fields to block"""
        pass

    def render_fields():
        """ Returns fields to render"""
        pass


class DexterityView(DefaultView, BrowserView):
    """
    Customizable browser view
    """

    @property
    def block_fields(self):
        block_fields = self.request.get('block_fields', None)
        if not block_fields:
            content_type = self.context.portal_type
            block_pairs = api.portal.get_registry_record('medialog.dexterityview.interfaces.IDexterityViewSettings.content_pairs')
            if block_pairs:
                for pair in block_pairs:
                    if pair['content_type'] == content_type:
                        if pair['block_fields'] != None:
                            return pair['block_fields']

        return ('IBasic.title', 'IBasic.description', 'title', 'description')

    @property
    def render_fields(self):
        return self.request.get('render_fields', '')


class ImageScale(BrowserView):
    """
    Helper view for the widget. Must be a better way to do this.
    """

    def __call__(self):
        content_type = self.context.portal_type
        content_pairs = api.portal.get_registry_record('medialog.dexterityview.interfaces.IDexterityViewSettings.content_pairs')
        for pair in content_pairs:
            if pair['content_type'] == content_type:
                if pair['image_scale'] != None:
                    return pair['image_scale']

        return 'preview'