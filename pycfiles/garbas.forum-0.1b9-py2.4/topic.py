# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/content/topic.py
# Compiled at: 2008-09-25 22:13:53
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.exceptions import AccessControl_Unauthorized
from garbas.forum.content.base import ForumFolder
from garbas.forum.content.base import ForumFolderSchema
from garbas.forum.interfaces import IForumTopic
from garbas.forum.interfaces import IForum
from garbas.forum.config import PROJECTNAME
from garbas.forum import ForumMessageFactory as _
TopicSchema = ForumFolderSchema.copy() + atapi.Schema((atapi.TextField(name='text', required=True, searchable=True, default_output_type='text/x-html-safe', storage=atapi.AnnotationStorage(), widget=atapi.TextAreaWidget(label=_('topic_label_text', default='Text'), description=_('topic_help_text', default='Write text.'))),))
TopicSchema['description'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}

class ForumTopic(ForumFolder):
    """forum topic content"""
    __module__ = __name__
    implements(IForumTopic)
    portal_type = 'ForumTopic'
    schema = TopicSchema
    title = atapi.ATFieldProperty('title')
    text = atapi.ATFieldProperty('text')


atapi.registerType(ForumTopic, PROJECTNAME)