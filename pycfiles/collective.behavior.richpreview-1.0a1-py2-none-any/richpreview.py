# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/behavior.richpreview/src/collective/behavior/richpreview/browser/richpreview.py
# Compiled at: 2018-04-05 17:11:04
from collective.behavior.richpreview.behaviors import IRichPreview
from collective.behavior.richpreview.interfaces import IRichPreviewSettings
from lxml import etree
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from requests.exceptions import RequestException
from zope.publisher.browser import BrowserView
import json, requests
TIMEOUT = 5

class RichPreviewJsonView(BrowserView):
    """Helper view to return page metadata in JSON format."""

    def setup(self):
        self.url = self.request.get('url', '')

    def get_meta_property(self, name):
        meta = self.html.find('*/meta[@property="' + name + '"]')
        if meta is None:
            return ''
        else:
            return meta.attrib.get('content', '')

    def extract_data(self):
        """Extracts metadata from the page."""
        try:
            r = requests.get(url=self.url, timeout=TIMEOUT)
        except RequestException:
            return {}

        if r.status_code != 200:
            return {}
        self.html = etree.HTML(r.content)
        title = self.get_meta_property('og:title')
        description = self.get_meta_property('og:description')
        image = self.get_meta_property('og:image')
        if not all((image, title)):
            return {}
        return {'title': title, 
           'description': description, 
           'image': image}

    def __call__(self):
        self.setup()
        if not self.url:
            self.request.RESPONSE.setStatus(400)
            return ''
        response = self.request.RESPONSE
        response.setHeader('Content-Type', 'application/json')
        return response.setBody(json.dumps(self.extract_data()))


class RichPreviewViewlet(ViewletBase):
    """Viewlet with rich preview templates and settings."""

    @property
    def enabled(self):
        if not IRichPreview.providedBy(self.context):
            return False
        record = IRichPreviewSettings.__identifier__ + '.enable'
        enabled = api.portal.get_registry_record(record)
        return api.user.is_anonymous() and enabled