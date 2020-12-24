# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/collective/namedblobfile/interfaces.py
# Compiled at: 2008-04-23 22:44:43
from collective.namedfile.interfaces import INamedFile

class INamedBlobFile(INamedFile):
    __module__ = __name__


class INamedBlobImage(INamedBlobFile):
    __module__ = __name__