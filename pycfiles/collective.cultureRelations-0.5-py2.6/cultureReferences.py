# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/cultureRelations/browser/cultureReferences.py
# Compiled at: 2011-03-08 08:07:28
import time, string, math
from Acquisition import aq_inner
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from collective.flowplayer.interfaces import IFlowPlayable
from collective.flowplayer.interfaces import IFlowPlayable
from collective.flowplayer.interfaces import IAudio
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName

class References(ViewletBase):
    render = ViewPageTemplateFile('cultureReferences.pt')

    def update(self):
        self.computed_value = 'any output'

    def shouldActivate(self):
        """Defines if the viewlet should show or not
        """
        if hasattr(self.view, 'clearsReferences'):
            return view.clearsReferences()
        else:
            return self.context.restrictedTraverse('@@plone_context_state').is_view_template()

    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def tag(self, obj, css_class='tileImage'):
        context = aq_inner(obj)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None:
            if field.get_size(context) != 0:
                scale = 'mini'
                return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def getValidTypes(self):
        properties_tool = getToolByName(self.context, 'portal_properties', None)
        if properties_tool is not None:
            references_properties = getattr(properties_tool, 'references_properties', None)
            if references_properties:
                if references_properties.hasProperty('apply_to'):
                    types = references_properties.apply_to
                    return types
        return []

    def isValidType(self, type):
        types = self.getValidTypes()
        if type in types:
            return True
        else:
            return False

    def getStrategicTypesByContext(self):
        currentType = self.context.portal_type
        types = []
        if currentType == 'Event':
            types.append('Document')
            types.append('File')
        elif currentType == 'Person' or currentType == 'Organization':
            types.append('Work')
            types.append('Event')
            types.append('Document')
            types.append('News Item')
            types.append('File')
        elif currentType == 'Work':
            types.append('Person')
            types.append('Event')
        return types

    def getAllRelatedItemsOfTypes(self, types):
        results = []
        for type in types:
            typeItems = self.getRelatedItemsByType(type)
            for item in typeItems:
                results.append(item)
                if type == 'Work':
                    innerEvents = self.getWorkRelatedEvents(item)
                    for ev in innerEvents:
                        results.append(ev)

        resultNoRepeated = self.uniq(results)
        return resultNoRepeated

    def translateMonth(self, month):
        if self.request['LANGUAGE'][:2] == 'en':
            return month
        if self.request['LANGUAGE'][:2] == 'es':
            if month == 'Jan':
                return 'Ene'
            else:
                if month == 'Apr':
                    return 'Abr'
                if month == 'Aug':
                    return 'Ago'
                if month == 'Dec':
                    return 'Dic'
                return month
        else:
            return month

    def getWorkRelatedPeople(self, work):
        result = []
        if work.portal_type == 'Work':
            related = work.getRefs()
            backRelated = work.getBRefs()
            related.extend(backRelated)
            for item in related:
                if item.portal_type == 'Person' or item.portal_type == 'Organization':
                    result.append(item)

        resultNoRepeated = self.uniq(result)
        return resultNoRepeated

    def getWorkRelatedEvents(self, work):
        result = []
        if work.portal_type == 'Work':
            related = work.getRefs()
            backRelated = work.getBRefs()
            related.extend(backRelated)
            for item in related:
                if item.portal_type == 'Event':
                    result.append(item)

        resultNoRepeated = self.uniq(result)
        return resultNoRepeated

    def currenttime(self):
        return time.time()

    def trimDescription(self, desc, num):
        if len(desc) > num:
            res = desc[0:num]
            lastspace = res.rfind(' ')
            res = res[0:lastspace] + ' ...'
            return res
        else:
            return desc

    def isPublishable(self, item):
        if item.getPortalTypeName() == 'File' or item.getPortalTypeName() == 'Image':
            return False
        else:
            return True

    def getRelatedItemsByType(self, type):
        related = self.context.getRefs()
        backRelated = self.context.getBRefs()
        result = []
        workflow = getToolByName(self, 'portal_workflow')
        member = getToolByName(self, 'portal_membership')
        for backItem in backRelated:
            if self.getTypeName(backItem.getPortalTypeName()) == self.getTypeName(type) and (not self.isPublishable(backItem) or workflow.getInfoFor(backItem, 'review_state') == 'published' or not member.isAnonymousUser()):
                if backItem.id != self.context.id:
                    result.append(backItem)

        for item in related:
            if self.getTypeName(item.getPortalTypeName()) == self.getTypeName(type) and (not self.isPublishable(item) or workflow.getInfoFor(item, 'review_state') == 'published' or not member.isAnonymousUser()):
                if item.id != self.context.id:
                    result.append(item)

        return self.uniq(result)

    def uniq(self, alist):
        set = {}
        return [ set.setdefault(e, e) for e in alist if e not in set ]

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        try:
            return util.ulocalized_time(time, long_format, time_only, self.context, domain='plonelocales')
        except TypeError:
            return util.ulocalized_time(time, long_format, self.context, domain='plonelocales')

    def creator(self):
        return self.context.Creator()

    def author(self):
        return 0

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

    def getTypeName(self, type):
        if self.request['LANGUAGE'][:2] == 'es':
            if type == 'Person':
                name = 'Personas'
            elif type == 'Event':
                name = 'Eventos'
            elif type == 'Organization':
                name = 'Personas'
            elif type == 'Work':
                name = 'Obras'
            elif type == 'All':
                name = 'Todo'
            elif type == 'Media':
                name = 'Media'
            elif type == 'News Item':
                name = 'Noticias'
            elif type == 'Folder':
                name = 'Folderish'
            elif type == 'Topic':
                name = 'Folderish'
            else:
                name = type + 's'
        elif type == 'Person':
            name = 'People'
        elif type == 'Event':
            name = 'Events'
        elif type == 'Organization':
            name = 'People'
        elif type == 'Work':
            name = 'Works'
        elif type == 'All':
            name = 'All'
        elif type == 'Media':
            name = 'Media'
        elif type == 'News Item':
            name = 'News'
        elif type == 'Folder':
            name = 'Folderish'
        elif type == 'Topic':
            name = 'Folderish'
        else:
            name = type + 's'
        return name

    def getFolderImages(self, folderItem):
        catalog = getToolByName(self, 'portal_catalog')
        physicalPath = folderItem.getPhysicalPath()
        folderURL = ('/').join(physicalPath)
        catResults = catalog.searchResults(path={'query': folderURL, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                                 'File'))
        results = []
        for item in catResults:
            if item.portal_type == 'Image' or item.portal_type == 'File' and IFlowPlayable.providedBy(item.getObject()):
                results.append(item)

        return results

    def purgeTypes(self, types):
        names = []
        purged = []
        for item in types:
            if self.getTypeName(item) not in names:
                names.append(self.getTypeName(item))
                purged.append(item)

        return purged

    def isVideo(self, item):
        result = IFlowPlayable.providedBy(item)
        return result

    def audio_only(self, item):
        result = IAudio.providedBy(item)
        return result

    def getOrderedTypes(self):
        result = [
         'Event', 'Work', 'Person', 'Organization', 'Document', 'Folder']
        putils = getToolByName(self, 'plone_utils')
        types = putils.getUserFriendlyTypes()
        for item in types:
            if item not in result:
                result.append(item)

        purgedResult = self.purgeTypes(result)
        return purgedResult

    def normalizeString(self, str):
        return self.context.plone_utils.normalizeString(str)

    def hasContentLeadImage(self, obj):
        field = obj.getField(IMAGE_FIELD_NAME)
        if field is not None:
            value = field.get(obj)
            return not not value
        else:
            return