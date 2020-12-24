# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iscorpio/plonepm/content/PPMProject.py
# Compiled at: 2010-03-26 05:41:47
"""PPMProject defines a software project in Agile approach."""
__docformat__ = 'plaintext'
import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import TextField
from Products.Archetypes.public import RichWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import InAndOutWidget
from Products.Archetypes.public import LinesWidget
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATFolderSchema
from Products.ATContentTypes.configuration import zconf
from Products.CMFCore.utils import getToolByName
from iscorpio.plonepm.config import PROJECTNAME
from iscorpio.plonepm.interfaces import IPPMProject
__author__ = 'Sean Chen'
__email__ = 'chyxiang@gmail.com'
PPMProjectSchema = ATFolderSchema.copy() + Schema((TextField('xppm_text', searchable=True, required=True, default_output_type='text/x-html-safe', widget=RichWidget(label='Project body', rows=22)), LinesField('xppm_developers', searchable=False, required=True, vocabulary='vocabulary_allMembersList', widget=InAndOutWidget(label='Developers', descrpiton='Please select developers for this project')), LinesField('xppm_modules', searchable=False, required=True, widget=LinesWidget(label='Project Modules', description='Please specify the module for your project, one per line', cols=40)), StringField('xppm_repo_url', searchable=True, required=False, widget=StringWidget(label='Source Code Repository', description='Where you keep tracking your source code for this project', cols=50)), StringField('xppm_browse_code_url', searchable=True, required=False, widget=StringWidget(label='Source Code Browoser', description='Where you can browse your source code from Web browser', cols=50)), IntegerField('xppm_unique_sequence', default=0, widget=IntegerWidget(label='Unique Sequence', description='This sequence will generate unique ids for all artifacts in this project.'))))
finalizeATCTSchema(PPMProjectSchema)
PPMProjectSchema.changeSchemataForField('xppm_unique_sequence', 'settings')

class PPMProject(ATFolder):
    """PPMProject defines a software project following eXtreme
    Programming's idea/concept.
    """
    __module__ = __name__
    schema = PPMProjectSchema
    __implements__ = (
     ATFolder.__implements__,)
    implements(IPPMProject)
    meta_type = 'PPMProject'
    portal_type = 'PPMProject'
    archetype_name = 'PPMProject'
    _at_rename_after_creation = True
    log = logging.getLogger('PlonePM Project')
    security = ClassSecurityInfo()
    security.declarePublic('getNextUniqueId')

    def getNextUniqueId(self):
        """ Return the next value from the unique sequence, and
            update the sequence itself.
        """
        newId = self.xppm_unique_sequence + 1
        self.setXppm_unique_sequence(newId)
        return newId

    def getProjectRoot(self):
        """
        Returns the project object ieself.
        """
        return self

    def getCurrentMember(self):
        """
        returns current authenticated user.
        """
        mtool = getToolByName(self, 'portal_membership')
        return mtool.getAuthenticatedMember()

    def vocabulary_allMembersList(self):
        """ Return a list of tuple (user_id, fullname, email) for all
        the members of the portal.
        """
        members = []
        portalMembers = getToolByName(self, 'portal_membership')
        members = [ (member.id, member.getProperty('fullname', member.id), member.getProperty('email', None)) for member in portalMembers.listMembers() ]
        return DisplayList(members)

    def vocabulary_allStoriesList(self):
        """ Returns a display list for all stories, the format is like this:
        [id, id + title].
        """
        retList = [
         ('', '')]
        stories = self.getAllStories()
        for story in stories:
            retList.append((story.id, story.id + ' - ' + story.Title))

        self.log.debug('we got %s stories', len(retList))
        return DisplayList(retList)

    security.declarePublic('vocabulary_iterations')

    def vocabulary_iterations(self):
        """
        returns all iterations for this project as display list.
        """
        retList = []
        iterations = self.xpCatalogSearch(portal_type='PPMIteration')
        for iteration in iterations:
            retList.append((iteration.id, iteration.id + ' - ' + iteration.Title))

        return DisplayList(retList)

    security.declarePublic('vocabulary_useCases')

    def vocabulary_useCases(self):
        """
        returns all use cases for this project as display list.
        """
        retList = []
        cases = self.xpCatalogSearch(portal_type='PPMUseCase')
        for case in cases:
            retList.append((case.id, case.id + ' - ' + case.Title))

        return DisplayList(retList)

    security.declarePublic('getProjectDevelopers')

    def getProjectDevelopers(self):
        """ returns all developers for this project.
        """
        return self.getXppm_developers()

    security.declarePublic('getIteration')

    def getIteration(self, iterationId):
        """
        returns the iteration object for the given iteration id.
        """
        return getattr(self, iterationId)

    security.declarePublic('getAllIterations')

    def getAllIterations(self):
        """
        returns all iterations in this project.
        """
        return self.contentValues(filter={'portal_type': ['PPMIteration']})

    security.declarePublic('getStory')

    def getStory(self, storyId):
        """
        returns the story object for the given story id.
        """
        return getattr(self, storyId)

    security.declarePublic('getAllStories')

    def getAllStories(self, iteration=None):
        """ Return all Stories in this project.
        """
        query = {}
        query['portal_type'] = 'PPMStory'
        if iteration:
            query['getXppm_iteration'] = iteration
        return self.xpCatalogSearch(query)

    security.declarePublic('getAllSysReqs')

    def getAllSysReqs(self):
        """
        Return all system requirement in this project.
        """
        return self.xpCatalogSearch(portal_type='PPMSysReq')

    security.declarePublic('getUseCase')

    def getUseCase(self, caseId):
        """
        returns the use case object for the given use case id.
        """
        return getattr(self, caseId)

    security.declarePublic('getAllUseCases')

    def getAllUseCases(self):
        """
        Return all use cases in this project.
        """
        return self.xpCatalogSearch(portal_type='PPMUseCase')

    security.declarePublic('getMetadataTypes')

    def getMetadataTypes(self):
        """
        return a list of unique metadata types used for this project.
        """
        catalog = getToolByName(self, 'portal_catalog')
        return catalog.uniqueValuesFor('getXppm_metadata_type')

    security.declarePublic('getMetadata')

    def getMetadata(self, type=None):
        """
        this will return a catalog search result based on the
        given metadata type.  If the no type provide, all metadata
        will be returned.
        """
        query = {}
        query['portal_type'] = 'PPMMetadata'
        if type:
            query['getXppm_metadata_type'] = type
        return self.xpCatalogSearch(query)

    security.declarePublic('getMetadataTupleList')

    def getMetadataTupleList(self, type=None):
        metadata = [ (one.id, one.Title) for one in self.getMetadata(type) ]
        return metadata

    security.declarePublic('getMetadataById')

    def getMetadataById(self, theId):
        """
        return an unique metadata by the given id.
        """
        query = {'id': theId}
        oneMetadata = self.xpCatalogSearch(query)[0]
        return oneMetadata

    security.declarePublic('xpCatalogSearch')

    def xpCatalogSearch(self, criteria=None, **kwargs):
        """ returns the catalog search result based on the provided criteria
        or kwargs.
        """
        if criteria is None:
            criteria = kwargs
        else:
            criteria = dict(criteria)
        availableCriteria = {'id': 'getId', 'text': 'SearchableText', 'portal_type': 'portal_type', 'metadata_type': 'getXppm_metadata_type', 'iteration': 'getXppm_iteration', 'sort_on': 'sort_on', 'sort_order': 'sort_order', 'sort_limit': 'sort_limit'}
        query = {}
        query['path'] = ('/').join(self.getPhysicalPath())
        for (k, v) in availableCriteria.items():
            if k in criteria:
                query[v] = criteria[k]
            elif v in criteria:
                query[v] = criteria[v]

        catalog = getToolByName(self, 'portal_catalog')
        return catalog.searchResults(query)


registerType(PPMProject, PROJECTNAME)