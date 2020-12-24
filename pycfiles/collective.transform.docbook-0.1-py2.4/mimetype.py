# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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