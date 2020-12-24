# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/garbas/forum/content/forum.py
# Compiled at: 2008-09-25 18:30:46
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from garbas.forum.content.base import ForumFolder
from garbas.forum.content.base import ForumFolderSchema
from garbas.forum.interfaces import IForum
from garbas.forum.config import PROJECTNAME
from garbas.forum import ForumMessageFactory as _
ForumSchema = ForumFolderSchema.copy() + atapi.Schema((atapi.LinesField(name='categories', required=False, storage=atapi.AnnotationStorage(), widget=atapi.LinesWidget(label=_('categories_label', default='Categories'), description=_('categories_help', default='Write categories (one in each line) in order of appearing.'))), atapi.StringField(name='category', required=False, storage=atapi.AnnotationStorage(), widget=atapi.SelectionWidget(label=_('category_label', default='Category'), description=_('category_help', default='Select category in which forum you are just creating, should appear.'), format='select'), vocabulary='getAvaliableCategories'), atapi.BooleanField(name='allow_addtopic', default=True, storage=atapi.AnnotationStorage(), widget=atapi.BooleanWidget(label=_('allow_addtopic_label', default='Allow to add topic'), description=_('allow_addtopic_help', default='If checked you are allowing user to add topic to forum. This option is useful when you are creating forum container and you dont want to have any topic inside your container.')))))

class Forum(ForumFolder):
    """forum content"""
    __module__ = __name__
    implements(IForum)
    portal_type = 'Forum'
    schema = ForumSchema
    security = ClassSecurityInfo()
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    categories = atapi.ATFieldProperty('categories')
    category = atapi.ATFieldProperty('category')
    allow_addtopic = atapi.ATFieldProperty('allow_addtopic')
    security.declarePublic('getAvaliableCategories')

    def getAvaliableCategories(self):
        parent = self.getParentNode()
        avaliable_categories = [_('no_category', default='No category')]
        if parent.portal_type == 'Forum':
            for category in parent.categories:
                avaliable_categories.append(category.decode('utf-8'))

        return avaliable_categories


atapi.registerType(Forum, PROJECTNAME)