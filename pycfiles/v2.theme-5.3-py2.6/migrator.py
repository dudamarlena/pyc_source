# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/v2/theme/migrator.py
# Compiled at: 2010-11-26 10:19:45
"""XML migration script by David Jonas
This script migrates XML files into Plone Objects according to V2 Migration Structure"""
import libxml2, urllib2, AccessControl, transaction, time, sys
from DateTime import DateTime
from plone.i18n.normalizer import idnormalizer
from Testing.makerequest import makerequest
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
    from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
    from collective.contentleadimage.interfaces import ILeadImageable
    import collective.contentleadimage
    LEADIMAGE_EXISTS = True
except ImportException:
    LEADIMAGE_EXISTS = False

class PersonItem:
    """ Class to store a person from the xml file"""

    def __init__(self):
        self.firstname = ''
        self.middlename = ''
        self.lastname = ''
        self.intro = ''
        self.body = ''
        self.tags = ''
        self.nickname = ''
        self.nationality = ''
        self.image = ''
        self.caption = ''
        self.person_class = ''
        self.links = []

    def firstName(self):
        if self.firstname != '':
            return self.firstname
        else:
            if self.nickname != '':
                return self.nickname
            if self.lastname != '':
                self.firstname = self.lastname
                self.lastname = ''
                return self.firstname
            if self.middlename != '':
                self.firstname = self.middlename
                self.middlename = ''
                return self.firstname
            return ''

    def fullName(self):
        return self.firstname + ' ' + self.middlename + ' ' + self.lastname

    def description(self):
        nationality = ''
        if self.nationality != '':
            nationality = ' (%s)' % (self.nationality,)
        person_class_list = self.person_class.replace('  ', ' ').split(' ')
        person_class_list_last = person_class_list[(len(person_class_list) - 1)]
        person_class = self.person_class.replace('  ', ' ').replace(' ', ', ').replace(', ' + person_class_list_last, ' and ' + person_class_list_last)
        if self.person_class != '' and (self.person_class[:1] == 'a' or self.person_class[:1] == 'e' or self.person_class[:1] == 'i' or self.person_class[:1] == 'o' or self.person_class[:1] == 'u'):
            return self.fullName() + nationality + ' is an ' + person_class + '.'
            return self.fullName() + nationality + ' is a ' + person_class + '.'
        else:
            if nationality == '':
                return ''
            else:
                return self.fullName() + nationality + '.'

    def Body(self):
        links = ''
        if len(self.links) > 0:
            links = '<br /><br /><b>Links:</b><br />'
            for link in self.links:
                links = links + '<br />' + '<a href="' + link + '">' + link + '</a>'

        return self.intro + self.body + links


class ImageItem:
    """Class to store an Image from the xml file"""

    def __init__(self):
        self.title = ''
        self.subtitle = ''
        self.uri = ''
        self.tags = ''
        self.domains = ''


class WorkItem:
    """Class to store a Work from the xml file"""

    def __init__(self):
        self.title = ''
        self.subtitle = ''
        self.body = ''
        self.tags = ''
        self.image = ''
        self.caption = ''
        self.link = ''
        self.year = ''
        self.description = ''

    def Title(self):
        if self.year != '':
            return self.title + ' (%s)' % self.year
        else:
            return self.title

    def Body(self):
        if self.link == '':
            return self.body
        else:
            return self.body + '<br /><a href="' + self.link + '">' + self.link + '</a>'


class EventItem:
    """Class to store an Event from the xml file"""

    def __init__(self):
        self.title = ''
        self.subtitle = ''
        self.body = ''
        self.tags = ''
        self.image = ''
        self.caption = ''
        self.location = ''
        self.startDate = ''
        self.endDate = ''
        self.description = ''
        self.link = ''
        self.event_class = ''

    def Description(self):
        if self.subtitle != '':
            return self.subtitle
        else:
            if self.event_class != '':
                return self.event_class
            return ''


class OrganizationItem:
    """Class to store an Organization from the xml file"""

    def __init__(self):
        self.title = ''
        self.subtitle = ''
        self.body = ''
        self.tags = ''
        self.image = ''
        self.caption = ''
        self.link = ''
        self.organization_class = ''

    def Body(self):
        if self.link == '':
            return self.body
        else:
            return self.body + '<br /><a href="' + self.link + '">' + self.link + '</a>'

    def description(self):
        organization_class_list = self.organization_class.replace('  ', ' ').split(' ')
        organization_class_list_last = organization_class_list[(len(organization_class_list) - 1)]
        organization_class = self.organization_class.replace('  ', ' ').replace(' ', ', ').replace(', ' + organization_class_list_last, ' and ' + organization_class_list_last)
        if self.organization_class != '' and (self.organization_class[:1] == 'a' or self.organization_class[:1] == 'e' or self.organization_class[:1] == 'i' or self.organization_class[:1] == 'o' or self.organization_class[:1] == 'u'):
            return self.title + ' is an ' + organization_class.replace('_', ' ') + '. ' + self.subtitle
            return self.title + ' is a ' + organization_class.replace('_', ' ') + '. ' + self.subtitle
        else:
            return self.subtitle + '.'


class PageItem:
    """Class to store a Page from the xml file"""

    def __init__(self):
        self.title = ''
        self.link = ''
        self.body = ''
        self.tags = ''
        self.image = ''
        self.caption = ''
        self.description = ''

    def Body(self):
        if self.link == '':
            return self.body
        else:
            return self.body + '<br /><a href="' + self.link + '">' + self.link + '</a>'


class XMLMigrator:
    """ Gets an XML file, parses it and creates the content in the chosen plone instance """

    def __init__(self, portal, xmlFilePath, typeToCreate, folder):
        """Constructor that gets access to both the parsed file and the chosen portal"""
        print 'INITIALIZING CONTENT MIGRATOR'
        self.portal = portal
        self.xmlDoc = libxml2.parseFile(xmlFilePath)
        self.typeToCreate = typeToCreate
        self.folderPath = folder.split('/')
        self.errors = 0
        self.created = 0
        self.skipped = 0

    def cleanUp(self):
        self.xmlDoc.freeDoc()

    def getContainer(self):
        if len(self.folderPath) == 0:
            print 'Folder check failed'
            return None
        else:
            container = self.portal
            for folder in self.folderPath:
                if hasattr(container, folder):
                    container = container[folder]
                else:
                    print '== Chosen folder ' + folder + ' does not exist. Creating new folder =='
                    container.invokeFactory(type_name='Folder', id=folder, title='migration of type: ' + self.typeToCreate)
                    container = container[folder]

            return container

    def getOrCreateFolder(self, container, folderId, publish):
        if folderId != '':
            try:
                if hasattr(container, folderId):
                    container = container[folderId]
                else:
                    print '== Creating new folder =='
                    container.invokeFactory(type_name='Folder', id=folderId, title=folderId)
                    container = container[folderId]
                    if publish:
                        container.portal_workflow.doActionFor(container, 'publish', comment='content automatically published by migrationScript')
                return container
            except:
                print 'Folder %s could not be created: %s' % (folderId, sys.exc_info()[1])
                return

        else:
            return
        return

    def addLeadImage(self, item, image):
        if LEADIMAGE_EXISTS and image != '':
            try:
                imageFile = urllib2.urlopen(image)
                imageData = imageFile.read()
                urlSplit = image.split('/')
                filename = urlSplit[(len(urlSplit) - 1)]
                if ILeadImageable.providedBy(item):
                    field = aq_inner(item).getField(IMAGE_FIELD_NAME)
                    field.set(item, imageData, filename=filename)
                else:
                    print 'Item type does not accept leadImage'
                imageFile.close()
                return
            except:
                print 'LeadImage URL not available. LeadImage not created because: (' + image + ')', sys.exc_info()[1]
                return

    def addLeadImageCaption(self, item, caption):
        if LEADIMAGE_EXISTS and caption != '':
            try:
                if ILeadImageable.providedBy(item):
                    field = aq_inner(item).getField(IMAGE_CAPTION_FIELD_NAME)
                    field.set(item, caption)
                else:
                    print 'Item type does not accept leadImage therefore captions will be ignored'
            except:
                print 'Error adding leadImage caption: ', sys.exc_info()[1]

    def createPerson(self, person):
        transaction.begin()
        container = self.getContainer()
        dirtyId = person.firstname + ' ' + person.middlename + ' ' + person.lastname
        counter = 1
        result = False
        if person.description() == '' or person.image == '' or person.Body() == '':
            container = self.getOrCreateFolder(container, 'toReview', False)
        try:
            id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
            while hasattr(container, id) and id != '':
                print 'Object ' + id + ' already exists.'
                counter = counter + 1
                dirtyId = person.firstname + ' ' + person.middlename + ' ' + person.lastname + str(counter)
                id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
                print 'creating ' + id + ' instead'

            if counter > 1:
                container = self.getContainer()
                container = self.getOrCreateFolder(container, 'toReview', False)
            if not hasattr(container, id):
                container.invokeFactory(type_name='Person', id=id, firstName=person.firstName(), middleName=person.middlename, lastName=person.lastname, description=person.description())
                item = container[id]
                item.setText(person.Body())
                self.addLeadImage(item, person.image)
                self.addLeadImageCaption(item, person.caption)
                item.setSubject(person.tags.split(','))
                if person.description() != '' and person.image != '' and person.Body() != '' and counter == 1:
                    item.portal_workflow.doActionFor(item, 'publish', comment='Content automatically published by migrationScript')
                transaction.commit()
                result = True
                self.created = self.created + 1
        except:
            self.errors = self.errors + 1
            print 'Unexpected error on createPerson (' + dirtyId + '):', sys.exc_info()[1]
            transaction.abort()
            return result
        else:
            if not result:
                transaction.abort()
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId

        return result

    def createWork(self, work):
        transaction.begin()
        container = self.getContainer()
        dirtyId = work.Title()
        counter = 1
        result = False
        if work.subtitle == '' or work.image == '' or work.Body() == '':
            container = self.getOrCreateFolder(container, 'toReview', False)
        try:
            id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
            while hasattr(container, id) and id != '':
                print 'Object ' + id + ' already exists.'
                counter = counter + 1
                dirtyId = work.Title() + str(counter)
                id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
                print 'creating ' + id + ' instead'

            if counter > 1:
                container = self.getContainer()
                container = self.getOrCreateFolder(container, 'toReview', False)
            if not hasattr(container, id):
                container.invokeFactory(type_name='Work', id=id, title=work.Title(), description=work.subtitle)
                item = container[id]
                item.setText(work.Body())
                self.addLeadImage(item, work.image)
                self.addLeadImageCaption(item, work.caption)
                item.setSubject(work.tags.split(','))
                if work.subtitle != '' and work.image != '' and work.Body() != '' and counter == 1:
                    item.portal_workflow.doActionFor(item, 'publish', comment='Content automatically published by migrationScript')
                transaction.commit()
                result = True
                self.created = self.created + 1
        except:
            self.errors = self.errors + 1
            print 'Unexpected error on createWork (' + dirtyId + '):', sys.exc_info()[1]
            transaction.abort()
            return result
        else:
            if not result:
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId

        return result

    def createOrganization(self, organization):
        transaction.begin()
        container = self.getContainer()
        dirtyId = organization.title
        counter = 1
        result = False
        if organization.description() == '' or organization.image == '' or organization.body == '':
            container = self.getOrCreateFolder(container, 'toReview', False)
        try:
            id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
            while hasattr(container, id) and id != '':
                print 'Object ' + id + ' already exists.'
                counter = counter + 1
                dirtyId = organization.title + str(counter)
                id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
                print 'creating ' + id + ' instead'

            if counter > 1:
                container = self.getContainer()
                container = self.getOrCreateFolder(container, 'toReview', False)
            if not hasattr(container, id):
                container.invokeFactory(type_name='Organization', id=id, title=organization.title, description=organization.description())
                item = container[id]
                item.setText(organization.body)
                self.addLeadImage(item, organization.image)
                self.addLeadImageCaption(item, organization.caption)
                item.setSubject(organization.tags.split(','))
                if organization.description() != '' and organization.image != '' and organization.body != '' and counter == 1:
                    item.portal_workflow.doActionFor(item, 'publish', comment='Content automatically published by migrationScript')
                transaction.commit()
                result = True
                self.created = self.created + 1
        except:
            self.errors = self.errors + 1
            print 'Unexpected error on createOrganization (' + dirtyId + '):', sys.exc_info()[1]
            transaction.abort()
            return result
        else:
            if not result:
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId

        return result

    def createPage(self, page):
        transaction.begin()
        container = self.getContainer()
        dirtyId = page.title
        counter = 1
        result = False
        if page.description == '' or page.image == '' or page.Body() == '':
            container = self.getOrCreateFolder(container, 'toReview', False)
        try:
            id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
            while hasattr(container, id) and id != '':
                print 'Object ' + id + ' already exists.'
                counter = counter + 1
                dirtyId = page.title + str(counter)
                id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
                print 'creating ' + id + ' instead'

            if counter > 1:
                container = self.getContainer()
                container = self.getOrCreateFolder(container, 'toReview', False)
            if not hasattr(container, id):
                container.invokeFactory(type_name='Document', id=id, title=page.title, description=page.description)
                item = container[id]
                item.setText(page.Body())
                self.addLeadImage(item, page.image)
                self.addLeadImageCaption(item, page.caption)
                item.setSubject(page.tags.split(','))
                if page.description != '' and page.image != '' and page.Body() != '' and counter == 1:
                    item.portal_workflow.doActionFor(item, 'publish', comment='Content automatically published by migrationScript')
                transaction.commit()
                result = True
                self.created = self.created + 1
        except:
            self.errors = self.errors + 1
            print 'Unexpected error on createPage (' + dirtyId + '):', sys.exc_info()[1]
            transaction.abort()
            return result
        else:
            if not result:
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId

        return result

    def createEvent(self, event):
        transaction.begin()
        container = self.getContainer()
        dirtyId = event.title
        result = False
        counter = 1
        if event.Description() == '' or event.image == '' or event.body == '':
            container = self.getOrCreateFolder(container, 'toReview', False)
        try:
            id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
            while hasattr(container, id) and id != '':
                print 'Object ' + id + ' already exists.'
                counter = counter + 1
                dirtyId = event.title + str(counter)
                id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
                print 'creating ' + id + ' instead'
                if counter > 4:
                    break

            if counter > 1:
                container = self.getContainer()
                container = self.getOrCreateFolder(container, 'toReview', False)
            if not hasattr(container, id):
                if event.endDate == '':
                    event.endDate = event.startDate
                container.invokeFactory(type_name='Event', id=id, title=event.title, description=event.Description(), startDate=DateTime(event.startDate), endDate=DateTime(event.endDate))
                item = container[id]
                item.setText(event.body)
                self.addLeadImage(item, event.image)
                self.addLeadImageCaption(item, event.caption)
                item.setSubject(event.tags.split(','))
                if event.location != '':
                    item.location = event.location
                if event.Description() != '' and event.image != '' and event.body != '' and counter == 1:
                    item.portal_workflow.doActionFor(item, 'publish', comment='Content automatically published by migrationScript')
                transaction.commit()
                result = True
                self.created = self.created + 1
        except:
            self.errors = self.errors + 1
            print 'Unexpected error on createEvent: (' + dirtyId + ')', sys.exc_info()[1]
            transaction.abort()
            return result
        else:
            if not result:
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId

        return result

    def createImage(self, image):
        transaction.begin()
        container = self.getContainer()
        storage = container
        pathToStorage = []
        years = []
        events = []
        if image.domains != '':
            for folderName in image.domains:
                if folderName.isdigit():
                    years.append(folderName)
                elif folderName != '':
                    events.append(folderName)

        if len(years) > 1:
            smallest = 9999
            for year in years:
                if int(year) < smallest:
                    smallest = int(year)

            pathToStorage.append(str(smallest))
        elif len(years) == 0:
            pathToStorage.append('undated')
        else:
            pathToStorage.append(years[0])
        if len(events) == 0:
            pathToStorage.append('uncategorized')
        else:
            for event in events:
                pathToStorage.append(event)

            for folderId in pathToStorage:
                container = self.getOrCreateFolder(container, folderId, False)

            ids = container.objectIds()
            if len(ids) >= 5000:
                pathToStorage[len(pathToStorage) - 1] = pathToStorage[(len(pathToStorage) - 1)] + '-2'
                container = self.getContainer()
                for folderId in pathToStorage:
                    container = self.getOrCreateFolder(container, folderId, True)

            dirtyId = image.title
            result = False
            if image.uri == '':
                print 'Image has no URI, Skipping'
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId
                return result
        try:
            id = idnormalizer.normalize(unicode(dirtyId, 'utf-8'))
            if id == '':
                pathComponents = image.uri.split('/')
                filename = pathComponents[(len(pathComponents) - 1)]
                id = filename[:-4]
            if not hasattr(container, id):
                container.invokeFactory(type_name='Image', id=id, title=image.title)
                try:
                    item = container[id]
                    imageFile = urllib2.urlopen(image.uri)
                    imageData = imageFile.read()
                    item.edit(file=imageData)
                    imageFile.close()
                    item.setSubject(image.tags.split(','))
                except urllib2.HTTPError:
                    print 'Image URL not available, Skipping'
                    self.skipped = self.skipped + 1
                    print 'Skipped item: ' + dirtyId
                    return result
                else:
                    transaction.commit()
                    result = True
                    self.created = self.created + 1
        except:
            self.errors = self.errors + 1
            print 'Unexpected error on createImage (' + dirtyId + '): ', sys.exc_info()[1]
            transaction.abort()
            return result
        else:
            if not result:
                self.skipped = self.skipped + 1
                print 'Skipped item: ' + dirtyId

        return result

    def migrateToPerson(self):
        root = self.xmlDoc.children
        for field in root.children:
            if field.name == 'node':
                currentPerson = PersonItem()
                for personField in field.children:
                    if personField.name == 'firstname':
                        currentPerson.firstname = personField.content
                    elif personField.name == 'middlename':
                        currentPerson.middlename = personField.content
                    elif personField.name == 'lastname':
                        currentPerson.lastname = personField.content
                    elif personField.name == 'tags':
                        currentPerson.tags = personField.content + ', migratedV1'
                    elif personField.name == 'intro':
                        currentPerson.intro = personField.content
                    elif personField.name == 'body':
                        currentPerson.body = personField.content
                    elif personField.name == 'nickname':
                        currentPerson.nickname = personField.content
                    elif personField.name == 'location':
                        currentPerson.nationality = personField.content
                    elif personField.name == 'image':
                        currentPerson.image = personField.content
                    elif personField.name == 'caption':
                        currentPerson.caption = personField.content
                    elif personField.name == 'link':
                        currentPerson.links.append(personField.content)
                    elif personField.name == 'extra':
                        if personField.prop('field') == 'mmv2:person_classes':
                            currentPerson.person_class = personField.content.replace('/', ' ').strip()

                self.createPerson(currentPerson)

    def migrateToImage(self):
        root = self.xmlDoc.children
        for field in root.children:
            if field.name == 'node':
                currentImage = ImageItem()
                for imageField in field.children:
                    if imageField.name == 'link':
                        currentImage.uri = imageField.content
                    elif imageField.name == 'tags':
                        currentImage.tags = imageField.content + ', migratedV1'
                    elif imageField.name == 'extra':
                        if imageField.prop('field') == 'mmv2:imagedigital_title':
                            currentImage.title = imageField.content
                        if imageField.prop('field') == 'mmv2:imagedigital_smalltitle':
                            currentImage.subtitle = imageField.content
                        if imageField.prop('field') == 'mmv2:imagedigital_domains':
                            currentImage.domains = imageField.content.strip('/').split('//')

                self.createImage(currentImage)

    def migrateToWork(self):
        root = self.xmlDoc.children
        for field in root.children:
            if field.name == 'node':
                currentWork = WorkItem()
                for workField in field.children:
                    if workField.name == 'title':
                        currentWork.title = workField.content
                    elif workField.name == 'subtitle':
                        currentWork.subtitle = workField.content
                    elif workField.name == 'tags':
                        currentWork.tags = workField.content + ', migratedV1'
                    elif workField.name == 'body':
                        currentWork.body = workField.content
                    elif workField.name == 'image':
                        currentWork.image = workField.content
                    elif workField.name == 'caption':
                        currentWork.caption = workField.content
                    elif workField.name == 'start':
                        currentWork.year = workField.content[:4]
                    elif workField.name == 'description':
                        currentWork.description = workField.content

                self.createWork(currentWork)

    def migrateToOrganization(self):
        root = self.xmlDoc.children
        for field in root.children:
            if field.name == 'node':
                currentOrganization = OrganizationItem()
                for organizationField in field.children:
                    if organizationField.name == 'tags':
                        currentOrganization.tags = organizationField.content + ', migratedV1'
                    elif organizationField.name == 'title':
                        currentOrganization.title = organizationField.content
                    elif organizationField.name == 'subtitle':
                        currentOrganization.subtitle = organizationField.content
                    elif organizationField.name == 'link':
                        currentOrganization.link = organizationField.content
                    elif organizationField.name == 'body':
                        currentOrganization.body = organizationField.content
                    elif organizationField.name == 'image':
                        currentOrganization.image = organizationField.content
                    elif organizationField.name == 'caption':
                        currentOrganization.caption = organizationField.content
                    elif organizationField.name == 'extra':
                        if organizationField.prop('field') == 'mmv2:organisation_classes':
                            currentOrganization.organization_class = organizationField.content.replace('/', ' ').strip()

                self.createOrganization(currentOrganization)

    def migrateToEvent(self):
        root = self.xmlDoc.children
        for field in root.children:
            if field.name == 'node':
                currentEvent = EventItem()
                for eventField in field.children:
                    if eventField.name == 'tags':
                        currentEvent.tags = eventField.content + ', migratedV1'
                    elif eventField.name == 'title':
                        currentEvent.title = eventField.content
                    elif eventField.name == 'subtitle':
                        currentEvent.subtitle = eventField.content
                    elif eventField.name == 'link':
                        currentEvent.link = eventField.content
                    elif eventField.name == 'body':
                        currentEvent.body = eventField.content
                    elif eventField.name == 'image':
                        currentEvent.image = eventField.content
                    elif eventField.name == 'caption':
                        currentEvent.caption = eventField.content
                    elif eventField.name == 'date':
                        currentEvent.startDate = eventField.content
                    elif eventField.name == 'enddate':
                        currentEvent.endDate = eventField.content
                    elif eventField.name == 'location':
                        currentEvent.location = eventField.content
                    elif eventField.name == 'extra':
                        if eventField.prop('field') == 'mmv2:event_classes':
                            currentEvent.event_class = eventField.content.replace('/', ' ').replace('_', ' ').strip()

                self.createEvent(currentEvent)

    def migrateToPage(self):
        root = self.xmlDoc.children
        for field in root.children:
            if field.name == 'node':
                currentPage = PageItem()
                for pageField in field.children:
                    if pageField.name == 'title':
                        currentPage.title = pageField.content
                    elif pageField.name == 'tags':
                        currentPage.tags = pageField.content + ', migratedV1'
                    elif pageField.name == 'body':
                        currentPage.body = pageField.content
                    elif pageField.name == 'image':
                        currentPage.image = pageField.content
                    elif pageField.name == 'caption':
                        currentPage.caption = pageField.content
                    elif pageField.name == 'description':
                        currentPage.description = pageField.content
                    elif pageField.name == 'link':
                        currentPage.link = pageField.content

                self.createPage(currentPage)

    def startMigration(self):
        if self.portal is not None:
            if self.typeToCreate == 'Person':
                self.migrateToPerson()
            elif self.typeToCreate == 'Image':
                self.migrateToImage()
            elif self.typeToCreate == 'Work':
                self.migrateToWork()
            elif self.typeToCreate == 'Organization':
                self.migrateToOrganization()
            elif self.typeToCreate == 'Page':
                self.migrateToPage()
            elif self.typeToCreate == 'Event':
                self.migrateToEvent()
            else:
                print 'TYPE NOT RECOGNIZED!! ==>> ' + self.typeToCreate
            self.cleanUp()
        else:
            print 'Portal is NONE!!!'
            self.cleanUp()
        return