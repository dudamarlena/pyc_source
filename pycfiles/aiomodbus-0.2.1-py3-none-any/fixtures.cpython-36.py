# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/denny/project/picme/aiommy/build/lib/tests/fixtures.py
# Compiled at: 2017-11-20 03:41:06
# Size of source mod 2**32: 840 bytes
import peewee, peewee_async
from aiommy.unittest import ModelTestCase
TEST_DB = peewee_async.PooledPostgresqlDatabase('test_db',
  user='denny')

class TestModel(peewee.Model):
    objects = peewee_async.Manager(TEST_DB)

    class Meta:
        table_name = 'test_table'
        database = TEST_DB


class ExtendedTestModel(TestModel):
    data1 = peewee.IntegerField()
    data2 = peewee.CharField(max_length=20)


class TestingPaginationModel(peewee.Model):
    date = peewee.DateTimeField()

    class Meta:
        db_table = 'test_table'


class PaginationTestCase(ModelTestCase):

    def setUp(self):
        TestingPaginationModel._meta.database = self.database
        TestingPaginationModel.objects = peewee_async.Manager(self.database)
        self.models.append(TestingPaginationModel)
        super().setUp()