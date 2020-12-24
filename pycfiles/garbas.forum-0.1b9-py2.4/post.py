# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/content/post.py
# Compiled at: 2008-09-25 18:53:20
from zope.interface import implements
from Products.Archetypes import atapi
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from garbas.forum.config import PROJECTNAME
from garbas.forum import ForumMessageFactory as _
from garbas.forum.interfaces import IForumPost
PostSchema = ATDocumentSchema.copy() + atapi.Schema((atapi.TextField(name='text', storage=atapi.AnnotationStorage(), searchable=True, default_output_type='text/x-html-safe', widget=atapi.TextAreaWidget(label=_('topic_label_text', default='Text'), description=_('topic_help_text', default='Write text.'))),))
PostSchema['title'].storage = atapi.AnnotationStorage()
PostSchema['title'].default = 'getDefaultTitle'
PostSchema['description'].storage = atapi.AnnotationStorage()
PostSchema['description'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
finalizeATCTSchema(PostSchema)

class ForumPost(ATDocument):
    """forum post content
    """
    __module__ = __name__
    implements(IForumPost)
    portal_type = 'ForumPost'
    _at_rename_after_creation = True
    schema = PostSchema
    title = atapi.ATFieldProperty('title')
    text = atapi.ATFieldProperty('text')

    def getDefaultTitle(self):
        return 'RE: ' + self.getParentNode().Title()


atapi.registerType(ForumPost, PROJECTNAME)