# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/browser/widget/converter.py
# Compiled at: 2012-06-20 11:31:01
from cStringIO import StringIO
from PIL import Image
from z3c.form.interfaces import IWidget, NOT_CHANGED
from ztfy.file.interfaces import IFileField, IImageField, ICthumbImageField, ICthumbImageFieldData
from z3c.form.converter import FileUploadDataConverter, FormatterValidationError
from zope.component import adapts
from zope.interface import implements
from zope.publisher.browser import FileUpload
from ztfy.file.display import ThumbnailGeometry
from ztfy.file import _

class FileFieldDataConverter(FileUploadDataConverter):
    """Data converter for FileField fields"""
    adapts(IFileField, IWidget)

    def toWidgetValue(self, value):
        if isinstance(value, tuple):
            value = value[0]
        return super(FileFieldDataConverter, self).toWidgetValue(value)

    def toFieldValue(self, value):
        if isinstance(value, FileUpload):
            filename = value.filename
        else:
            filename = None
        result = super(FileFieldDataConverter, self).toFieldValue(value)
        if result is NOT_CHANGED:
            widget = self.widget
            if widget.deleted:
                return
            return result
        else:
            return filename and (result, filename) or result
        return


class ImageFieldDataConverter(FileFieldDataConverter):
    """Data converter for ImageField fields"""
    adapts(IImageField, IWidget)

    def toFieldValue(self, value):
        result = super(ImageFieldDataConverter, self).toFieldValue(value)
        test_result = isinstance(result, tuple) and result[0] or result
        if test_result is not None and test_result is not NOT_CHANGED:
            try:
                Image.open(StringIO(test_result))
            except:
                raise FormatterValidationError(_('Given file is not in a recognized image format'), value)

        return result


class CthumbImageFieldData(object):
    implements(ICthumbImageFieldData)

    def __init__(self, value, geometry):
        self.value = value
        self.geometry = geometry

    def __nonzero__(self):
        return bool(self.value)


class CthumbImageFieldDataConverter(FileFieldDataConverter):
    """Data converter for CthumbImageField fields"""
    adapts(ICthumbImageField, IWidget)

    def toFieldValue(self, value):
        result = super(CthumbImageFieldDataConverter, self).toFieldValue(value)
        widget = self.widget
        return CthumbImageFieldData(result, ThumbnailGeometry(widget.position, widget.size))