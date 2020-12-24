# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/dbsprockets/test/testViewFactory.py
# Compiled at: 2008-06-30 11:43:30
from dbsprockets.viewfactory import ViewFactory
from dbsprockets.viewconfig import ViewConfig
from dbsprockets.metadata import Metadata, NotFoundError
from dbsprockets.iprovider import IProvider

class DummyMetadata(Metadata):

    def _doKeys(self):
        return []


class DummyViewConfig(ViewConfig):
    metadataType = DummyMetadata


class testViewFactory:

    def setup(self):
        provider = IProvider()
        self.viewFactory = ViewFactory()
        self.viewConfig = DummyViewConfig(provider, 'test_table')

    def testCreateObj(self):
        pass

    def testCreate(self):
        view = self.viewFactory.create(self.viewConfig)