# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.markdown/medialog/markdown/browser/views.py
# Compiled at: 2018-02-07 06:06:26
from Products.Five.browser import BrowserView
from plone import api

class RenderFromMarkdown(BrowserView):
    """ mardown to html.
    """

    def __call__(self, *args, **kw):
        return self.render_markdown()

    def render_markdown(self, markdown=''):
        """Return the preview as a stringified HTML document."""
        value = self.request.markdown
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        data = portal_transforms.convertTo('text/html', value, mimetype='text/x-web-markdown')
        html = data.getData()
        return html