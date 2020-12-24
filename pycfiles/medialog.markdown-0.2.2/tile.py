# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.markdown/medialog/markdown/tiles/tile.py
# Compiled at: 2018-02-07 06:06:26
from plone import api
from plone.memoize.view import memoize
from plone.supermodel import model
from zope import schema
from plone.directives import form
from zope.i18nmessageid import MessageFactory
from plone.tiles import Tile
from zope.schema import getFields
from medialog.markdown.interfaces import IMarkdownSettings
from medialog.markdown.widgets.widget import MarkdownFieldWidget
_ = MessageFactory('medialog.markdownn')

class IMarkdownTile(model.Schema):
    bodytext = schema.Text(title='Body text')
    form.widget(bodytext=MarkdownFieldWidget)


class MarkdownTile(Tile):
    """A tile that displays markdown text"""

    def __init__(self, context, request):
        super(MarkdownTile, self).__init__(context, request)

    def render_markdown(self):
        """Return the preview as a stringified HTML document."""
        value = self.data['bodytext']
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        html = portal_transforms.convertTo('text/html', value, mimetype='text/x-web-markdown')
        return html.getData()