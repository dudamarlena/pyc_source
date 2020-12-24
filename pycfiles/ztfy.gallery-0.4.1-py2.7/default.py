# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/defaultskin/renderers/default.py
# Compiled at: 2013-03-09 17:52:00
__docformat__ = 'restructuredtext'
from ztfy.blog.defaultskin.layer import IZBlogDefaultLayer
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.gallery.interfaces import IGalleryContainer, IGalleryParagraph, IGalleryParagraphRenderer, IGalleryManagerPaypalInfo
from z3c.template.template import getViewTemplate
from zope.component import adapts
from zope.interface import implements
from zope.traversing import api as traversing_api
from ztfy.gallery.defaultskin import ztfy_gallery_defaultskin_css
from ztfy.jqueryui import jquery_tools_12, jquery_fancybox
from ztfy.utils.request import setRequestData
from ztfy.utils.traversing import getParent
from ztfy.gallery import _

class DefaultGalleryParagraphRenderer(object):
    adapts(IGalleryParagraph, IZBlogDefaultLayer)
    implements(IGalleryParagraphRenderer)
    label = _('Default gallery renderer with small slides')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        self.gallery = IGalleryContainer(traversing_api.getParent(self.context))
        ztfy_gallery_defaultskin_css.need()
        jquery_tools_12.need()
        jquery_fancybox.need()

    render = getViewTemplate()

    @property
    def paypal(self):
        site = getParent(self.context, ISiteManager)
        info = IGalleryManagerPaypalInfo(site)
        setRequestData('gallery.paypal', info, self.request)
        return info