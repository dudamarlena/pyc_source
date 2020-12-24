# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/adi/samplecontent/setuphandlers.py
# Compiled at: 2012-12-02 02:48:44


def deleteDefaultContent(p):
    """Deletes default contents
    """
    existing = p.objectIds()
    itemsToDelete = ['Members', 'news', 'events', 'front-page']
    for item in itemsToDelete:
        if item in existing:
            p.manage_delObjects(item)
            print 'adi.init-INSTALL-INFO: Deleted %s' % item
        else:
            print "adi.init-INSTALL-INFO: Skipped deletion of %s, doesn't exists." % item


def addSimpleContent(p):
    """ Add some sample content
    """
    existing = p.objectIds()
    contentIds = ['go-to-welcome', 'welcome', 'about', 'contact']
    contentExeptions = ['go-to-welcome', 'contact']
    for contentId in contentIds:
        contentTitle = str.capitalize(contentId)
        contentChild = contentId + '-info'
        if contentId not in existing:
            if contentId not in contentExeptions:
                p.invokeFactory(type_name='Folder', id=contentId, title=contentTitle)
                contekst = p[contentId]
                contekst.invokeFactory(type_name='Document', id=contentChild, title=contentTitle)
                contekst.setDefaultPage(contentChild)
            if contentId is 'go-to-welcome':
                p.invokeFactory(type_name='Link', id=contentId, title=contentId, remoteUrl='./welcome')
                p.setDefaultPage(contentId)
            if contentId is 'contact':
                p.invokeFactory(type_name='Folder', id=contentId, title=contentTitle)
                p.contact.setLayout(contentChild)
            print 'adi.init-INSTALL-INFO: Created %s' % contentId
        else:
            print 'adi.init-INSTALL-INFO: Skipped creation of %s, exists already.' % contentId

    print 'adi.init-INSTALL-INFO: *** Installation finished ***'


def setupVarious(context):
    portal = context.getSite()
    if context.readDataFile('adi.samplecontent.marker.txt') is None:
        return
    else:
        deleteDefaultContent(portal)
        addSimpleContent(portal)
        return