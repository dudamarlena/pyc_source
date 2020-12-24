# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/collective/flowplayercaptions/Extensions/install.py
# Compiled at: 2011-01-03 15:18:37
from zope import interface
from collective.flowplayercaptions.interfaces import ICaptionsSource

def uninstall(portal, reinstall=False):
    setup_tool = portal.portal_setup
    setup_tool.setBaselineContext('profile-collective.flowplayercaptions:uninstall')
    setup_tool.runAllImportStepsFromProfile('profile-collective.flowplayercaptions:uninstall')
    if not reinstall:
        removeFlowplayerCaptionsMarks(portal)


def removeFlowplayerCaptionsMarks(portal):
    """Remove all marker interfaces all around the site"""
    log = portal.plone_log
    catalog = portal.portal_catalog
    captionedContents = catalog(object_provides=ICaptionsSource.__identifier__)
    log('Uninstall Flowplayer captions support: removing merker on captioned video contents...')
    for captioned in captionedContents:
        content = captioned.getObject()
        interface.noLongerProvides(content, ICaptionsSource)
        content.reindexObject(['object_provides'])
        log('   unmarked %s' % ('/').join(content.getPhysicalPath()))

    log('...done. Thanks you for using me!')