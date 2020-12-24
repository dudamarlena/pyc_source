# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/topic.py
# Compiled at: 2013-09-21 08:56:34
__docformat__ = 'restructuredtext'
from zope.annotation.interfaces import IAnnotations
from ztfy.blog.interfaces.blog import IBlog
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.blog.interfaces.topic import ITopic
from ztfy.hplskin.interfaces import ISiteManagerPresentationInfo, IBlogPresentationInfo, ITopicPresentationInfo
from ztfy.hplskin.layer import IHPLLayer
from ztfy.skin.interfaces import IPresentationTarget
from zope.component import adapts
from zope.interface import implements
from zope.proxy import ProxyBase, setProxiedObject
from ztfy.blog.defaultskin.topic import TopicPresentation as BaseTopicPresentation, TopicIndexView as BaseTopicIndexView, TopicResourcesView as BaseTopicResourcesView, TopicCommentsView as BaseTopicCommentsView
from ztfy.hplskin.menu import HPLSkinDialogMenuItem
from ztfy.utils.traversing import getParent
from ztfy.hplskin import _
TOPIC_PRESENTATION_KEY = 'ztfy.hplskin.topic.presentation'

class TopicPresentationViewMenuItem(HPLSkinDialogMenuItem):
    """Topic presentation menu item"""
    title = _(' :: Presentation model...')


class TopicPresentation(BaseTopicPresentation):
    """Topic presentation infos"""
    implements(ITopicPresentationInfo)


class TopicPresentationAdapter(ProxyBase):
    adapts(ITopic)
    implements(ITopicPresentationInfo)

    def __init__(self, context):
        annotations = IAnnotations(context)
        presentation = annotations.get(TOPIC_PRESENTATION_KEY)
        if presentation is None:
            presentation = annotations[TOPIC_PRESENTATION_KEY] = TopicPresentation()
        setProxiedObject(self, presentation)
        return


class TopicPresentationTargetAdapter(object):
    adapts(ITopic, IHPLLayer)
    implements(IPresentationTarget)
    target_interface = ITopicPresentationInfo

    def __init__(self, context, request):
        self.context, self.request = context, request


class TopicIndexView(BaseTopicIndexView):
    """Topic index view"""
    pass


class TopicResourcesView(BaseTopicResourcesView):
    """Topic resources view"""

    @property
    def resources(self):
        return ITopicPresentationInfo(self.context).linked_resources


class TopicCommentsView(BaseTopicCommentsView):
    """Topic comments view"""

    @property
    def presentation(self):
        if not self.context.commentable:
            return
        else:
            site = getParent(self.context, ISiteManager)
            if site is not None:
                return ISiteManagerPresentationInfo(site)
            blog = getParent(self.context, IBlog)
            if blog is not None:
                return IBlogPresentationInfo(blog)
            return