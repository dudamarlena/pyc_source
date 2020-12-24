# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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