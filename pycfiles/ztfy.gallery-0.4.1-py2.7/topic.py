# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/skin/topic.py
# Compiled at: 2013-09-21 08:55:10
__docformat__ = 'restructuredtext'
from persistent import Persistent
from zope.annotation.interfaces import IAnnotations
from zope.intid.interfaces import IIntIds
from ztfy.blog.interfaces.site import ISiteManager
from ztfy.blog.interfaces.topic import ITopic
from ztfy.gallery.interfaces import IGalleryManagerPaypalInfo
from ztfy.gallery.skin.interfaces import ITopicPresentation, ITopicPresentationInfo
from ztfy.gallery.skin.layer import IGalleryLayer
from ztfy.skin.interfaces import IPresentationTarget
from zope.container.contained import Contained
from zope.component import adapter, adapts, getUtility
from zope.interface import implementer, implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.blog.defaultskin.topic import TopicIndexPreview as TopicIndexPreviewBase
from ztfy.gallery.skin.menu import GallerySkinDialogMenuItem
from ztfy.i18n.property import I18nTextProperty
from ztfy.jqueryui import jquery_tools_12, jquery_fancybox
from ztfy.utils.request import setData
from ztfy.utils.traversing import getParent
from ztfy.gallery import _
TOPIC_PRESENTATION_KEY = 'ztfy.gallery.presentation'

class TopicPresentationViewMenuItem(GallerySkinDialogMenuItem):
    """Topic presentation menu item"""
    title = _(' :: Presentation model...')


class TopicPresentation(Persistent, Contained):
    """Topic presentation infos"""
    implements(ITopicPresentation)
    publication_date = I18nTextProperty(ITopicPresentation['publication_date'])
    header_format = FieldProperty(ITopicPresentation['header_format'])
    display_googleplus = FieldProperty(ITopicPresentation['display_googleplus'])
    display_fb_like = FieldProperty(ITopicPresentationInfo['display_fb_like'])
    illustration_position = FieldProperty(ITopicPresentation['illustration_position'])
    illustration_width = FieldProperty(ITopicPresentation['illustration_width'])
    linked_resources = FieldProperty(ITopicPresentation['linked_resources'])


@adapter(ITopic)
@implementer(ITopicPresentation)
def TopicPresentationFactory(context):
    annotations = IAnnotations(context)
    presentation = annotations.get(TOPIC_PRESENTATION_KEY)
    if presentation is None:
        presentation = annotations[TOPIC_PRESENTATION_KEY] = TopicPresentation()
    return presentation


class TopicPresentationTargetAdapter(object):
    adapts(ITopic, IGalleryLayer)
    implements(IPresentationTarget)
    target_interface = ITopicPresentationInfo

    def __init__(self, context, request):
        self.context, self.request = context, request


class TopicIndexPreview(TopicIndexPreviewBase):

    def __call__(self, images=[]):
        self.images = images
        if images:
            jquery_tools_12.need()
            jquery_fancybox.need()
        return super(TopicIndexPreview, self).__call__()

    @property
    def oid(self):
        intids = getUtility(IIntIds)
        return intids.queryId(self.context)

    @property
    def pages(self):
        index = 0
        images = self.images
        length = len(images)
        while index < length:
            yield images[index:index + 5]
            index += 5

    @property
    def paypal(self):
        site = getParent(self.context, ISiteManager)
        info = IGalleryManagerPaypalInfo(site)
        setData('gallery.paypal', info, self.request)
        return info