# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/tests/sampledata.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.interface import implements
from zope.app.component.hooks import setSite
from zope.component import queryUtility, provideUtility
from z3c.sampledata.interfaces import ISampleDataPlugin
from ice.adverlet.interfaces import ISourceStorage, IFileStorage
from ice.adverlet.storage import SourceStorage, FileStorage

class SampleSourceStorage(object):
    __module__ = __name__
    implements(ISampleDataPlugin)
    name = 'ice.adverlet.sample.sourcestorage'
    dependencies = []
    schema = None

    def generate(self, context, param={}, dataSource=None, seed=None):
        setSite(context)
        storage = queryUtility(ISourceStorage)
        if storage is None:
            storage = SourceStorage()
            sm = context.getSiteManager()
            sm['source_storage'] = storage
            provideUtility(storage, ISourceStorage)
        return storage


class SampleFileStorage(object):
    __module__ = __name__
    implements(ISampleDataPlugin)
    name = 'ice.adverlet.sample.filestorage'
    dependencies = []
    schema = None

    def generate(self, context, param={}, dataSource=None, seed=None):
        setSite(context)
        storage = queryUtility(IFileStorage)
        if storage is None:
            storage = FileStorage()
            sm = context.getSiteManager()
            sm['file_storage'] = storage
            provideUtility(storage, IFileStorage)
        return storage