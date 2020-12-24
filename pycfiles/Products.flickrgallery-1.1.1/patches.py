# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\patches.py
# Compiled at: 2009-03-02 16:14:26
import mimetypes
from logging import getLogger
from Products.CMFPlone import utils
from Products.CMFCore.PortalFolder import PortalFolderBase
from Products.FlashVideo.config import FLASHVIDEO_PORTALTYPE
from Products.FlashVideo.config import PROJECTNAME
from Products.FlashVideo.config import FLASHVIDEO_MIMETYPE
log = getLogger(PROJECTNAME)
old_createObjectByType = utils._createObjectByType

def new_createObjectByType(type_name, container, id, *args, **kw):
    """
    Prevent ids from having dots inside for Flash Video objects.
    Flow Player doesn't like that.
    """
    if type_name == FLASHVIDEO_PORTALTYPE:
        id = id.replace('.', '_')
    return old_createObjectByType(type_name, container, id, *args, **kw)


log.info('Applying patch for Products.CMFPlone.utils._createObjectByType')
utils._createObjectByType = new_createObjectByType
mimetypes.add_type('video/x-flv', '.flv')