# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oleiade/Dev/Sandbox/Python/Elevator/tests/api_tests.py
# Compiled at: 2012-10-23 04:08:00
import unittest2, shutil, msgpack, os, leveldb
from nose.tools import *
from elevator.api import Handler
from elevator.db import DatabasesHandler
from elevator.constants import *
from elevator.message import Request, ResponseContent, ResponseHeader
from .fakers import gen_test_env

class ApiTests(unittest2.TestCase):

    def _bootstrap_db(self, db):
        for val in xrange(9):
            db.Put(str(val), str(val))

    def setUp(self):
        self.env = gen_test_env()
        self.databases = DatabasesHandler('/tmp/store.json', '/tmp')
        self.default_db_uid = self.databases.index['name_to_uid']['default']
        self._bootstrap_db(self.databases[self.default_db_uid]['connector'])
        self.handler = Handler(self.databases)

    def tearDown(self):
        shutil.rmtree('/tmp/default')
        os.remove('/tmp/store.json')

    def request_message(self, command, args, db_uid=None):
        db_uid = db_uid or self.default_db_uid
        return Request(msgpack.packb({'uid': db_uid, 
           'cmd': command, 
           'args': args}))

    def test_command_with_existing_command(self):
        message = self.request_message('GET', ['1'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertNotEqual(plain_content['datas'], None)
        return

    def test_command_with_non_existing_command(self):
        message = self.request_message('COTCOT', ['testarg'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], KEY_ERROR)

    def test_command_with_invalid_db_uid(self):
        message = self.request_message('PUT', ['1', '1'], db_uid='failinguid')
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], RUNTIME_ERROR)

    def test_get_of_existing_key(self):
        message = self.request_message('GET', ['1'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], ('1', ))

    def test_get_of_non_existing_key(self):
        message = self.request_message('GET', ['abc123'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], KEY_ERROR)

    def test_mget_of_existing_keys(self):
        message = self.request_message('MGET', [['1', '2', '3']])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], ('1', '2', '3'))

    def test_mget_of_not_fully_existing_keys(self):
        message = self.request_message('MGET', [['1', '2', 'touptoupidou']])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], WARNING_STATUS)
        self.assertEqual(len(plain_content['datas']), 3)
        self.assertEqual(plain_content['datas'], ('1', '2', None))
        return

    def test_put_of_valid_key(self):
        message = self.request_message('PUT', ['a', '1'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], None)
        return

    def test_put_of_existing_key(self):
        message = self.request_message('PUT', ['a', 1])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], TYPE_ERROR)

    def test_delete(self):
        message = self.request_message('DELETE', ['9'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], None)
        return

    def test_range(self):
        message = self.request_message('RANGE', ['1', '2'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertIsInstance(plain_content['datas'], tuple)
        self.assertEqual(plain_content['datas'][0], ('1', '1'))
        self.assertEqual(plain_content['datas'][1], ('2', '2'))

    def test_range_of_len_one(self):
        """Should still return a tuple of tuple"""
        message = self.request_message('RANGE', ['1', '1'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertIsInstance(plain_content['datas'], tuple)
        self.assertEqual(len(plain_content), 1)
        self.assertEqual(plain_content['datas'], (('1', '1'), ))

    def test_slice_with_limit(self):
        message = self.request_message('SLICE', ['1', 3])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertIsInstance(plain_content['datas'], tuple)
        self.assertEqual(len(plain_content['datas']), 3)
        self.assertEqual(plain_content['datas'][0], ('1', '1'))
        self.assertEqual(plain_content['datas'][1], ('2', '2'))
        self.assertEqual(plain_content['datas'][2], ('3', '3'))

    def test_slice_with_limit_value_of_one(self):
        message = self.request_message('SLICE', ['1', 1])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertIsInstance(plain_content['datas'], tuple)
        self.assertEqual(len(plain_content), 1)
        self.assertEqual(plain_content['datas'], (('1', '1'), ))

    def test_batch_with_valid_collection(self):
        message = self.request_message('BATCH', args=[
         [
          (
           SIGNAL_BATCH_PUT, 'a', 'a'),
          (
           SIGNAL_BATCH_PUT, 'b', 'b'),
          (
           SIGNAL_BATCH_PUT, 'c', 'c')]])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], None)
        return

    def test_batch_with_invalid_signals(self):
        message = self.request_message('BATCH', [
         [
          (-5, 'a', 'a'),
          (-5, 'b', 'b'),
          (-5, 'c', 'c')]])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], SIGNAL_ERROR)

    def test_batch_with_invalid_collection_datas_type(self):
        message = self.request_message('BATCH', [
         [
          (
           SIGNAL_BATCH_PUT, 'a', 1),
          (
           SIGNAL_BATCH_PUT, 'b', 2),
          (
           SIGNAL_BATCH_PUT, 'c', 3)]])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], TYPE_ERROR)

    def test_connect_to_valid_database(self):
        message = Request(msgpack.packb({'uid': None, 
           'cmd': 'DBCONNECT', 
           'args': [
                  'default']}))
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertIsNotNone(plain_content)
        return

    def test_connect_to_invalid_database(self):
        message = Request(msgpack.packb({'uid': None, 
           'cmd': 'DBCONNECT', 
           'args': [
                  'dadaislikeadad']}))
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], DATABASE_ERROR)
        return

    def test_connect_automatically_mounts_and_unmounted_db(self):
        db_uid = self.handler.databases.index['name_to_uid']['default']
        self.handler.databases[db_uid]['status'] = self.handler.databases.STATUSES.UNMOUNTED
        self.handler.databases[db_uid]['connector'] = None
        message = Request(msgpack.packb({'db_uid': None, 
           'cmd': 'DBCONNECT', 
           'args': [
                  'default']}))
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(self.handler.databases[db_uid]['status'], self.handler.databases.STATUSES.MOUNTED)
        self.assertIsInstance(self.handler.databases[db_uid]['connector'], leveldb.LevelDB)
        return

    def test_create_valid_db(self):
        message = self.request_message('DBCREATE', ['testdb'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], None)
        return

    def test_create_already_existing_db(self):
        message = self.request_message('DBCREATE', ['default'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], DATABASE_ERROR)

    def test_drop_valid_db(self):
        message = self.request_message('DBDROP', ['default'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(plain_content['datas'], None)
        os.mkdir('/tmp/default')
        return

    def test_drop_non_existing_db(self):
        message = self.request_message('DBDROP', ['testdb'])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], FAILURE_STATUS)
        self.assertEqual(plain_header['err_code'], DATABASE_ERROR)

    def test_list_db(self):
        message = self.request_message('DBLIST', [])
        header, content = self.handler.command(message)
        plain_header = msgpack.unpackb(header)
        plain_content = msgpack.unpackb(content)
        self.assertEqual(plain_header['status'], SUCCESS_STATUS)
        self.assertEqual(len(plain_content), 1)
        self.assertEqual(plain_content['datas'], ('default', ))