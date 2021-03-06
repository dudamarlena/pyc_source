# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/test_paginations/test_growing.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 3457 bytes
import datetime
from aiohttp.test_utils import unittest_run_loop
from aiommy.paginations.growing import GrowingPagination
from aiommy.unittest import ModelTestCase
from tests.fixtures import TEST_DB, TestingPaginationModel
PAGINATE_BY = 10

class GrowingPaginationTestCase(ModelTestCase):
    database = TEST_DB
    models = [TestingPaginationModel]

    def create_fixtures(self):
        self.objects_number = 50
        self.recomend_delta_for_testing = 25
        self.now = datetime.datetime.utcnow()
        objects = (dict(date=(self.now - datetime.timedelta(days=i))) for i in range(self.objects_number))
        TestingPaginationModel.insert_many(objects).execute()
        self.paginator = GrowingPagination((TestingPaginationModel.date), PAGINATE_BY,
          model=TestingPaginationModel)

    @unittest_run_loop
    async def test_next_page(self):
        queryset = TestingPaginationModel.select()
        through = self.now - datetime.timedelta(days=(self.recomend_delta_for_testing))
        paginated = self.paginator.next(queryset, through, self.recomend_delta_for_testing)
        self.assertEqual(len(paginated), PAGINATE_BY)
        for obj in paginated:
            self.assertGreaterEqual(obj.date, through)

    @unittest_run_loop
    async def test_previous_page(self):
        queryset = TestingPaginationModel.select()
        through = self.now - datetime.timedelta(days=(self.recomend_delta_for_testing))
        paginated = self.paginator.previous(queryset, through, self.recomend_delta_for_testing)
        self.assertGreater(len(paginated), PAGINATE_BY)
        for obj in paginated:
            self.assertLessEqual(obj.date, through)

    @unittest_run_loop
    async def test_first_page(self):
        queryset = TestingPaginationModel.select()
        paginated = self.paginator.first(queryset, None, None)
        self.assertEqual(len(paginated), PAGINATE_BY)

    @unittest_run_loop
    async def test_items_per_page(self):
        queryset = TestingPaginationModel.select()
        paginated = self.paginator.first(queryset, None, None)
        self.assertEqual(len(paginated), PAGINATE_BY)


class GrowingLastIdTestCase(ModelTestCase):
    database = TEST_DB
    models = [TestingPaginationModel]

    def create_fixtures(self):
        self.duplicated_date = datetime.datetime.utcnow() + datetime.timedelta(days=3)
        self.objects = [
         dict(id=1, date=(self.duplicated_date)),
         dict(id=2, date=(self.duplicated_date)),
         dict(id=3, date=(datetime.datetime.utcnow() + datetime.timedelta(days=1))),
         dict(id=4, date=(datetime.datetime.utcnow() + datetime.timedelta(days=2)))]
        TestingPaginationModel.insert_many(self.objects).execute()
        self.paginator = GrowingPagination((TestingPaginationModel.date), PAGINATE_BY,
          model=TestingPaginationModel)

    @unittest_run_loop
    async def test_last_id_pagination(self):
        last_id = 1
        queryset = TestingPaginationModel.select()
        paginated = self.paginator.next(queryset, self.duplicated_date, last_id)
        for obj in paginated:
            try:
                self.assertGreater(obj.date, self.duplicated_date)
            except AssertionError:
                self.assertGreater(obj.id, last_id)