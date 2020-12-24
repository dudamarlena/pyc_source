# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/fileimage/image/_field.py
# Compiled at: 2007-11-30 08:40:44
from zope import schema
from zope import component
from p4a.fileimage import file

class ImageField(file.FileField):
    """A field for representing an image.
    """
    __module__ = __name__

    def __init__(self, preferred_dimensions=None, **kw):
        super(ImageField, self).__init__(**kw)
        self.preferred_dimensions = preferred_dimensions