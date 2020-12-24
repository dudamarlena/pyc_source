# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/envs/conversocial/lib/python2.7/site-packages/mongopony/tests/test_collection.py
# Compiled at: 2015-09-09 03:09:16
from .base import ConnectionMixin
from unittest import TestCase
from ..collection import Collection
from .. import local_config

class People(Collection):
    collection_name = 'people'


class TestCollection(ConnectionMixin, TestCase):

    def setUp(self):
        super(TestCollection, self).setUp()
        db_name = local_config.db_prefix + '_db'
        self.client.drop_database(db_name)
        self.db = getattr(self.client, db_name)

    def test_unfiltered_count(self):
        self.db.people.insert({'first_name': 'Colin'})
        query_plan = People.prepare_query(self.db)
        self.assertEquals(1, query_plan.count())

    def test_filtered_count(self):
        self.db.people.insert({'first_name': 'Colin'})
        query_plan = People.prepare_query(self.db)
        query_plan.filter({'first_name': 'Colin'})
        self.assertEquals(1, query_plan.count())
        query_plan.filter({'first_name': 'Bob'})
        self.assertEquals(0, query_plan.count())