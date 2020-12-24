# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/z3c/resourcecollector/browser.py
# Compiled at: 2008-07-30 04:23:44
import time, zope.component
from zope.viewlet import viewlet
from zope.app.publisher.browser.fileresource import FileResource
from zope.app.form.browser.widget import renderElement
from interfaces import ICollectorUtility

class CollectorResource(FileResource):

    def __init__(self, request):
        self.request = request

    def GET(self):
        rs = zope.component.getUtility(ICollectorUtility, self.__name__)
        resources = rs.getResources(self.request)
        if rs.content_type is not None:
            self.request.response.setHeader('Content-Type', rs.content_type)
        secs = 31536000
        self.request.response.setHeader('Cache-Control', 'public,max-age=%s' % secs)
        t = time.time() + secs
        self.request.response.setHeader('Expires', time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(t)))
        return resources


class CollectorViewlet(viewlet.ViewletBase):

    @property
    def collector(self):
        return self.__name__

    def renderElement(self, url):
        return self.template % {'url': url}

    def render(self):
        originalHeader = self.request.response.getHeader('Content-Type')
        if originalHeader is None:
            originalHeader = 'text/html'
        rs = zope.component.getUtility(ICollectorUtility, self.collector)
        versionedresource = rs.getUrl(self.context, self.request)
        view = zope.component.getAdapter(self.request, name=self.collector)
        url = '%s?hash=%s' % (view(), versionedresource)
        script = self.renderElement(url)
        self.request.response.setHeader('Content-Type', originalHeader)
        return script


class JSCollectorViewlet(CollectorViewlet):
    """Render a link to include Javascript resources"""

    def renderElement(self, url):
        return renderElement('script', src=url, extra='type="text/javascript"', contents=' ')


class CSSCollectorViewlet(CollectorViewlet):
    """Render a link to include CSS resources"""
    media = 'screen'

    def renderElement(self, url):
        return renderElement('link', rel='stylesheet', href=url, media=self.media, extra='type="text/css"')


class CSSIECollectorViewlet(CollectorViewlet):
    """Renders a IE Only include CSS resource
    to set lower then just overwride ieVersion in your zcml"""
    ieVersion = None
    versionOperator = None

    def renderElement(self, url):
        if self.ieVersion is None:
            return '<!--[if IE]><link rel="stylesheet" type="text/css" href="%s" /><![endif]-->' % url
        elif self.versionOperator:
            _vo = '%s ' % self.versionOperator
        else:
            _vo = ''
            return '<!--[if %sIE %s]><link rel="stylesheet" type="text/css" href="%s" /><![endif]-->' % (
             _vo,
             self.ieVersion,
             url)
        return