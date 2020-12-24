# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/content/roundabouttour.py
# Compiled at: 2008-12-19 11:25:03
"""Definition of the RoundAbout Tour content type
"""
from zope.interface import implements, directlyProvides
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.Archetypes.atapi import *
from AccessControl import ClassSecurityInfo
from collective.roundabout import roundaboutMessageFactory as _
from collective.roundabout.interfaces import IRoundAboutTour
from collective.roundabout.config import PROJECTNAME
RoundAboutTourSchema = folder.ATFolderSchema.copy() + atapi.Schema((TextField(name='above_content', allowable_content_types=('text/html', ), widget=RichWidget(label='Above content', description='Text shown above the content', label_msgid='label_above_content', description_msgid='description_above_content', i18n_domain='collective.roundabout'), default_output_type='text/html', searchable=True), IntegerField(name='viewer_width', widget=IntegerField._properties['widget'](label='Viewer width', description='Width in pixels of the viewer', label_msgid='label_viewer_width', description_msgid='description_viewer_width', i18n_domain='collective.roundabout'), validators=('isInt', ), default='320', required=True), IntegerField(name='viewer_height', widget=IntegerField._properties['widget'](label='Viewer height', description='Height in pixels of the viewer', label_msgid='label_viewer_height', description_msgid='description_viewer_height', i18n_domain='collective.roundabout'), validators=('isInt', ), default='240', required=True), StringField(name='start_image', widget=SelectionWidget(label='Start image', description='Start image of the tour', label_msgid='label_start_image', description_msgid='description_start_image', i18n_domain='collective.roundabout', format='select'), vocabulary='_getImages'), FloatField(name='start_angle', widget=IntegerField._properties['widget'](label='Start angle', description='Start angle of the tour (between 0-360)', label_msgid='label_start_angle', description_msgid='description_start_angle', i18n_domain='collective.roundabout'), validators=('isDecimal', ), default='0', required=True), IntegerField(name='animation_frames', widget=IntegerField._properties['widget'](label='Animation frames', description='Number of frames in the animation between photos', label_msgid='label_animation_frames', description_msgid='description_animation_frames', i18n_domain='collective.roundabout'), validators=('isInt', ), default='10', required=True), TextField(name='below_content', allowable_content_types=('text/html', ), widget=RichWidget(label='Below content', description='Text shown below the content', label_msgid='label_below_content', description_msgid='description_below_content', i18n_domain='collective.roundabout'), default_output_type='text/html', searchable=True)))
RoundAboutTourSchema['title'].storage = atapi.AnnotationStorage()
RoundAboutTourSchema['description'].storage = atapi.AnnotationStorage()
schemata.finalizeATCTSchema(RoundAboutTourSchema, folderish=True, moveDiscussion=False)

class RoundAboutTour(folder.ATFolder):
    """Container for RoundAbout images and maps."""
    __module__ = __name__
    security = ClassSecurityInfo()
    implements(IRoundAboutTour)
    portal_type = 'RoundAbout Tour'
    schema = RoundAboutTourSchema
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    security.declarePrivate('_getImages')

    def _getImages(self):
        """Gets maps"""
        dl = DisplayList()
        parent = self.aq_inner
        for x in parent.getFolderContents():
            if x.portal_type == 'RoundAbout Image':
                dl.add(x.id, x.Title)

        return dl


atapi.registerType(RoundAboutTour, PROJECTNAME)