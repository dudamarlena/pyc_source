# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/collage/ploneformgen/browser.py
# Compiled at: 2011-01-28 06:57:46
from zope import interface
from zope import component
from Products.PloneFormGen.browser.embedded import EmbeddedPFGView
from Products.Collage.browser import helper
from Products.Collage.browser import views
from Products.Collage.viewmanager import mark_request
from Products.Collage.interfaces import IDynamicViewManager
from Acquisition import aq_inner
from ZPublisher.Publish import Retry

class PloneFormGenView(EmbeddedPFGView, views.BaseView):
    title = 'Standard'

    @property
    def prefix(self):
        return 'form-%s' % self.context.UID()

    @property
    def action(self):
        return self.helper.getCollageObject().absolute_url()

    @property
    def helper(self):
        return helper.CollageHelper(self.collage_context, self.request)

    @property
    def __call__(self):
        return self.index

    def render_embedded_view(self):
        try:
            return EmbeddedPFGView.__call__(self)
        except Retry:
            path_translated = self.request._orig_env['PATH_TRANSLATED']
            if 'VirtualHostRoot' in path_translated:
                nodes = path_translated.replace('/VirtualHostBase/', '').replace('/VirtualHostRoot', '').split('/')
                nodes = nodes[2:]
                path_translated = ('/').join(nodes)
            context = self.context.unrestrictedTraverse(path_translated)
            manager = IDynamicViewManager(context)
            layout = manager.getLayout()
            if not layout:
                (layout, title) = manager.getDefaultLayout()
            ifaces = mark_request(self.context, self.request)
            view = component.getMultiAdapter((context, self.request), name=layout)
            interface.directlyProvides(self.request, ifaces)
            return view()