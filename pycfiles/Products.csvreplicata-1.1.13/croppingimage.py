# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/croppingimage/croppingimage.py
# Compiled at: 2008-07-23 09:49:01
from cStringIO import StringIO
from cgi import FieldStorage
from AccessControl import ClassSecurityInfo
from ZPublisher.HTTPRequest import FileUpload
from Products.Archetypes.public import BaseContent, registerType
from schema import cropping_image_schema
from config import PROJECTNAME, CROPPING_IMAGE_TYPE, LONG_NAME, DESIRED_WIDTH, DESIRED_HEIGHT
import permissions as perms, PIL.Image

class CroppingImage(BaseContent):
    """An Image type that crops to specified dimensions.
    """
    __module__ = __name__
    security = ClassSecurityInfo()
    schema = cropping_image_schema
    meta_type = CROPPING_IMAGE_TYPE
    archetype_name = portal_type = LONG_NAME
    content_icon = 'image_icon.gif'


def _getFormat(filename):
    ext = '.%s' % filename.split('.')[(-1)].lower()
    try:
        format = PIL.Image.EXTENSION[ext]
    except KeyError:
        PIL.Image.init()
        try:
            format = PIL.Image.EXTENSION[ext]
        except KeyError:
            raise Exception(PIL.Image.EXTENSION)

    return format


registerType(CroppingImage, PROJECTNAME)