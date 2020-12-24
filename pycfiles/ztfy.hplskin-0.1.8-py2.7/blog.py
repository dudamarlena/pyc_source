# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/blog.py
# Compiled at: 2013-09-21 08:55:42
__docformat__ = 'restructuredtext'
from zope.annotation.interfaces import IAnnotations
from ztfy.blog.interfaces.blog import IBlog
from ztfy.hplskin.interfaces import IBlogPresentationInfo
from ztfy.hplskin.layer import IHPLLayer
from ztfy.skin.interfaces import IPresentationTarget
from zope.component import adapts
from zope.interface import implements
from zope.proxy import ProxyBase, setProxiedObject
from ztfy.blog.defaultskin.blog import BlogPresentation as BaseBlogPresentation, BlogIndexView as BaseBlogIndexView
from ztfy.hplskin.menu import HPLSkinDialogMenuItem
from ztfy.hplskin import _
BLOG_PRESENTATION_KEY = 'ztfy.hplskin.blog.presentation'

class BlogPresentationViewMenuItem(HPLSkinDialogMenuItem):
    """Blog presentation menu item"""
    title = _(' :: Presentation model...')


class BlogPresentation(BaseBlogPresentation):
    """Blog presentation infos"""
    implements(IBlogPresentationInfo)


class BlogPresentationAdapter(ProxyBase):
    adapts(IBlog)
    implements(IBlogPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(BLOG_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[BLOG_PRESENTATION_KEY] = BlogPresentation()
        setProxiedObject(self, presentation)
        return


class BlogPresentationTargetAdapter(object):
    adapts(IBlog, IHPLLayer)
    implements(IPresentationTarget)
    target_interface = IBlogPresentationInfo

    def __init__(self, context, request):
        self.context, self.request = context, request


class BlogIndexView(BaseBlogIndexView):
    """Blog index page"""
    pass