# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/storage.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from BTrees.OOBTree import OOBTree
from persistent import Persistent
from zope.interface import implements
from zope.app.container.contained import Contained
from zope.app.container.btree import BTreeContainer
from zope.schema.fieldproperty import FieldProperty
from interfaces import ISourceStorage, IFileStorage

class SourceStorage(Persistent, Contained):
    __module__ = __name__
    implements(ISourceStorage)
    mceplugins = FieldProperty(ISourceStorage['mceplugins'])
    defaultCSS = FieldProperty(ISourceStorage['defaultCSS'])

    def __init__(self):
        self.sources = OOBTree()


class FileStorage(BTreeContainer):
    __module__ = __name__
    implements(IFileStorage)