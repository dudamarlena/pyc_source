# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/collective/namedblobfile/blobimage.py
# Compiled at: 2008-04-23 22:44:43
from zope.interface import implements
from blobfile import NamedBlobFile
from interfaces import INamedBlobImage

class NamedBlobImage(NamedBlobFile):
    __module__ = __name__
    implements(INamedBlobImage)