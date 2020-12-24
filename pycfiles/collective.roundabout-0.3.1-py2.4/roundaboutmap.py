# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/content/roundaboutmap.py
# Compiled at: 2008-12-14 11:55:57
"""Definition of the RoundAbout Map content type
"""
from zope.interface import implements, directlyProvides
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import *
from AccessControl import ClassSecurityInfo
from collective.roundabout import roundaboutMessageFactory as _
from collective.roundabout.interfaces import IRoundAboutMap
from collective.roundabout.config import PROJECTNAME
RoundAboutMapSchema = folder.ATFolderSchema.copy() + atapi.Schema((ImageField(name='image', widget=PhotoField._properties['widget'](label='Image', description='Map image', label_msgid='label_map_image', description_msgid='description_map_image', i18n_domain='collective.roundabout'), storage=AttributeStorage(), max_size=(768,
                                                                                                                                                                                                                                                               768), sizes={'large': (768, 768), 'preview': (400, 400), 'mini': (200, 200), 'thumb': (128, 128), 'tile': (64, 64), 'icon': (32, 32), 'listing': (16, 16)}, required=True),))
RoundAboutMapSchema['title'].storage = atapi.AnnotationStorage()
RoundAboutMapSchema['description'].storage = atapi.AnnotationStorage()
schemata.finalizeATCTSchema(RoundAboutMapSchema, folderish=True, moveDiscussion=False)

class RoundAboutMap(folder.ATFolder):
    """RoundAbout Map"""
    __module__ = __name__
    security = ClassSecurityInfo()
    implements(IRoundAboutMap)
    portal_type = 'RoundAbout Map'
    schema = RoundAboutMapSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')


atapi.registerType(RoundAboutMap, PROJECTNAME)