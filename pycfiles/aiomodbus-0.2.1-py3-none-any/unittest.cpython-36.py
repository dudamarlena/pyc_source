# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/aiommy/unittest.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 2195 bytes
import asyncio, datetime, unittest, peewee_async
from aiohttp.test_utils import AioHTTPTestCase
from aiommy.dateutils import to_iso

class AioTestCase(unittest.TestCase):

    def setUp(self):
        self.now = to_iso(datetime.datetime.utcnow())
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()


class ModelTestCase(AioTestCase):
    models = []
    database = None

    def setUp(self):
        super().setUp()
        self.manager = peewee_async.Manager((self.database), loop=(self.loop))
        for m in self.models:
            m._meta.database = self.database
            m.objects = self.manager

        self.database.create_tables((self.models), safe=True)
        self.create_fixtures()

    def create_fixtures(self):
        """
        method for create fixtures,
        not implemented for base test case
        :return:
        """
        pass

    def tearDown(self):
        for m in self.models:
            self.loop.run_until_complete(m.objects.close())

        self.loop.run_until_complete(self.manager.close())
        self.database.drop_tables((self.models), safe=True, cascade=True)
        super().tearDownClass()


class IntegrationTestCase(AioHTTPTestCase):
    models = []
    database = None

    def get_app(self):
        raise NotImplementedError

    def setUp(self):
        super().setUp()
        self.now = to_iso(datetime.datetime.utcnow())
        self.manager = peewee_async.Manager((self.database), loop=(self.loop))
        for m in self.models:
            m._meta.database = self.database
            m.objects = self.manager

        self.database.create_tables((self.models), safe=True)
        self.create_fixtures()

    def create_fixtures(self):
        """
        method for create fixtures,
        not implemented for base test case
        :return:
        """
        pass

    def tearDown(self):
        for m in self.models:
            self.loop.run_until_complete(m.objects.close())

        self.loop.run_until_complete(self.manager.close())
        self.database.drop_tables((self.models), safe=True, cascade=True)
        super().tearDown()