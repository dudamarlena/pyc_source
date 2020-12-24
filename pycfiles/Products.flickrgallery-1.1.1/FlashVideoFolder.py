# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\content\FlashVideoFolder.py
# Compiled at: 2009-03-02 16:14:25
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.public import *
from Products.FlashVideo.config import *
FlashVideoFolderSchema = ATFolderSchema.copy()

class FlashVideoFolder(ATFolder):
    __module__ = __name__
    schema = FlashVideoFolderSchema
    content_icon = 'flashvideofolder_icon.gif'
    meta_type = FLASHVIDEOFOLDER_METATYPE
    portal_type = FLASHVIDEOFOLDER_PORTALTYPE
    archetype_name = FLASHVIDEOFOLDER_PORTALTYPE
    allowed_content_types = ()
    filter_content_types = 1
    immediate_view = 'flashvideofolder_view'
    default_view = 'flashvideofolder_view'
    filter_content_types = 1
    allowed_content_types = (FLASHVIDEO_PORTALTYPE, FLASHVIDEOPLAYLIST_PORTALTYPE)
    typeDescription = 'A folder which contains Flash video (*.flv) files and playlists.'
    typeDescMsgId = 'description_type_flashvideofolder'
    __implements__ = ATFolder.__implements__
    security = ClassSecurityInfo()


registerType(FlashVideoFolder, PROJECTNAME)