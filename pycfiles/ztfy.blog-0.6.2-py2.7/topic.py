# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/topic.py
# Compiled at: 2013-09-22 07:52:53
__docformat__ = 'restructuredtext'
from zope.dublincore.interfaces import IZopeDublinCore
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from ztfy.blog.interfaces.topic import ITopic
from zope.app.content import queryContentType
from zope.component import adapter
from zope.i18n import translate
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from ztfy.base.ordered import OrderedContainer
from ztfy.extfile.blob import BlobImage
from ztfy.i18n.property import I18nTextProperty, I18nImageProperty
from ztfy.utils.request import getRequest
from ztfy.blog import _

class Topic(OrderedContainer):
    implements(ITopic)
    title = I18nTextProperty(ITopic['title'])
    shortname = I18nTextProperty(ITopic['shortname'])
    description = I18nTextProperty(ITopic['description'])
    keywords = I18nTextProperty(ITopic['keywords'])
    heading = I18nTextProperty(ITopic['heading'])
    header = I18nImageProperty(ITopic['header'], klass=BlobImage, img_klass=BlobImage)
    illustration = I18nImageProperty(ITopic['illustration'], klass=BlobImage, img_klass=BlobImage)
    illustration_title = I18nTextProperty(ITopic['illustration_title'])
    commentable = FieldProperty(ITopic['commentable'])
    workflow_name = FieldProperty(ITopic['workflow_name'])

    @property
    def content_type(self):
        return queryContentType(self).__name__

    @property
    def paragraphs(self):
        return self.values()

    def getVisibleParagraphs(self, request=None):
        return [ v for v in self.paragraphs if v.visible ]

    @property
    def publication_year(self):
        return IZopeDublinCore(self).created.year

    @property
    def publication_month(self):
        return IZopeDublinCore(self).created.month


@adapter(ITopic, IObjectCreatedEvent)
def handleNewTopic(object, event):
    """Init workflow status of a new topic"""
    IWorkflowState(object).setState(None)
    IWorkflowInfo(object).fireTransition('init', translate(_('Create new topic'), context=getRequest()))
    return