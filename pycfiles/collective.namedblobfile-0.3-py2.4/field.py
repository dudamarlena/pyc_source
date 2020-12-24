# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/collective/namedblobfile/field.py
# Compiled at: 2008-04-23 22:44:43
from zope.interface import implements
from collective.namedfile.field import NamedFile, NamedImage, NamedFileProxy, NamedImageProxy
from interfaces import INamedBlobFile, INamedBlobImage
from blobfile import NamedBlobFile as BlobFileValueType
from blobimage import NamedBlobImage as BlobImageValueType

class NamedBlobFile(NamedFile):
    """A NamedBlobFile field
    """
    __module__ = __name__
    implements(INamedBlobFile)


class NamedBlobImage(NamedImage):
    """A NamedBlobImage field
    """
    __module__ = __name__
    implements(INamedBlobImage)


class NamedBlobFileProxy(NamedFileProxy):
    __module__ = __name__
    implements(INamedBlobFile)
    _valueType = BlobFileValueType


class NamedBlobImageProxy(NamedImageProxy):
    __module__ = __name__
    implements(INamedBlobImage)
    _valueType = BlobImageValueType