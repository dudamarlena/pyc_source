# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/schema.py
# Compiled at: 2012-06-20 11:31:01
from ztfy.file.interfaces import IHTMLField, IFileField, IImageField, ICthumbImageField
from zope.interface import implements
from zope.schema import Text, Bytes

class HTMLField(Text):
    """Custom field used to handle HTML properties"""
    implements(IHTMLField)


class FileField(Bytes):
    """Custom field used to handle file-like properties"""
    implements(IFileField)

    def _validate(self, value):
        pass


class ImageField(FileField):
    """Custom field used to handle image-like properties"""
    implements(IImageField)


class CthumbImageField(ImageField):
    """Custom field used to handle images with cthumb selection"""
    implements(ICthumbImageField)