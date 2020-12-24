# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/transform/docbook/mimetype.py
# Compiled at: 2009-03-11 14:14:44
from Products.MimetypesRegistry.interfaces import IClassifier
from Products.MimetypesRegistry.MimeTypeItem import MimeTypeItem
from Products.MimetypesRegistry.common import MimeTypeException
from types import InstanceType

class application_docbook(MimeTypeItem):
    __module__ = __name__
    __implements__ = MimeTypeItem.__implements__
    __name__ = 'DocBook'
    mimetypes = ('application/docbook+xml', )
    extensions = ('dbk', )
    binary = 0