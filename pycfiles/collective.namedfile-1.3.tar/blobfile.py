# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/collective/namedblobfile/blobfile.py
# Compiled at: 2008-04-23 22:44:43
from z3c.blobfile.file import File
from interfaces import INamedBlobFile
from zope.interface import implements

class NamedBlobFile(File):
    __module__ = __name__
    implements(INamedBlobFile)

    def __init__(self, data='', contentType='', filename=None):
        File.__init__(self, data, contentType)
        self.filename = filename