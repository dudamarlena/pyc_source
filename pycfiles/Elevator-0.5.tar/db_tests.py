# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oleiade/Dev/Sandbox/Python/Elevator/tests/db_tests.py
# Compiled at: 2012-10-23 04:08:00
from __future__ import absolute_import
import unittest2, os, json, shutil, tempfile, leveldb
from elevator.utils.snippets import from_mo_to_bytes
from elevator.constants import SUCCESS_STATUS, FAILURE_STATUS, KEY_ERROR, RUNTIME_ERROR, DATABASE_ERROR
from elevator.db import DatabasesHandler, DatabaseOptions
from .fakers import gen_test_env
from .utils import rm_from_pattern

class DatabaseOptionsTest(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class DatabasesTest(unittest2.TestCase):

    def setUp(self):
        self.store = '/tmp/store.json'
        self.dest = '/tmp/dbs'
        self.env = gen_test_env()
        if not os.path.exists(self.dest):
            os.mkdir(self.dest)
        self.handler = DatabasesHandler(self.store, self.dest)

    def tearDown(self):
        os.remove('/tmp/store.json')
        shutil.rmtree('/tmp/dbs')

    def test_init(self):
        self.assertIn('default', self.handler.index['name_to_uid'])
        default_db_uid = self.handler.index['name_to_uid']['default']
        self.assertEqual(self.handler[default_db_uid]['name'], 'default')
        self.assertEqual(self.handler[default_db_uid]['path'], '/tmp/dbs/default')

    def test_global_max_cache_size(self):
        self.assertEqual(self.handler.global_cache_size, 16)
        self.handler.add('test_cache', db_options={'block_cache_size': 8 * 2097152})
        self.assertEqual(self.handler.global_cache_size, 32)

    def test_load(self):
        db_name = 'testdb'
        self.handler.add(db_name)
        self.assertIn(db_name, self.handler.index['name_to_uid'])
        db_uid = self.handler.index['name_to_uid'][db_name]
        self.assertIn(db_uid, self.handler)
        self.assertEqual(self.handler[db_uid]['name'], db_name)
        self.assertIn('default', self.handler.index['name_to_uid'])

    def test_store_update(self):
        db_name = 'test_db'
        db_desc = {'path': '/tmp/test_path', 
           'uid': 'testuid', 
           'options': {}}
        self.handler.store_update(db_name, db_desc)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertIn(db_name, store_datas)
        self.assertEqual(store_datas[db_name], db_desc)

    def test_store_remove(self):
        db_name = 'test_db'
        db_desc = {'path': '/tmp/test_path', 
           'uid': 'testuid', 
           'options': {}}
        self.handler.store_update(db_name, db_desc)
        self.handler.store_remove(db_name)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertNotIn(db_name, store_datas)

    def test_drop_existing_db(self):
        db_name = 'default'
        status, content = self.handler.drop(db_name)
        self.assertEqual(status, SUCCESS_STATUS)
        self.assertEqual(content, None)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertNotIn(db_name, store_datas)
        return

    def test_remove_existing_db_which_files_were_erased(self):
        db_name = 'testdb'
        db_path = '/tmp/dbs/testdb'
        status, content = self.handler.add(db_name)
        shutil.rmtree(db_path)
        status, content = self.handler.drop(db_name)
        self.assertEqual(status, FAILURE_STATUS)
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], DATABASE_ERROR)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertNotIn(db_name, store_datas)

    def test_add_from_db_name_without_options_passed(self):
        db_name = 'testdb'
        default_db_options = DatabaseOptions()
        status, content = self.handler.add(db_name)
        self.assertEqual(status, SUCCESS_STATUS)
        self.assertEqual(content, None)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertIn(db_name, store_datas)
        self.assertEqual(store_datas[db_name]['path'], os.path.join(self.dest, db_name))
        self.assertIsNotNone(store_datas[db_name]['uid'])
        stored_db_options = store_datas[db_name]['options']
        self.assertIsNotNone(stored_db_options)
        self.assertIsInstance(stored_db_options, dict)
        for option_name, option_value in default_db_options.iteritems():
            self.assertIn(option_name, stored_db_options)
            self.assertEqual(option_value, stored_db_options[option_name])

        return

    def test_add_from_db_name_with_options_passed(self):
        db_name = 'testdb'
        db_options = DatabaseOptions(paranoid_checks=True)
        status, content = self.handler.add(db_name, db_options)
        self.assertEqual(status, SUCCESS_STATUS)
        self.assertEqual(content, None)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertIn(db_name, store_datas)
        self.assertEqual(store_datas[db_name]['path'], os.path.join(self.dest, db_name))
        self.assertIsNotNone(store_datas[db_name]['uid'])
        stored_db_options = store_datas[db_name]['options']
        self.assertIsNotNone(stored_db_options)
        self.assertIsInstance(stored_db_options, dict)
        for option_name, option_value in db_options.iteritems():
            if option_name == 'paranoid_check':
                self.assertEqual(option_value, False)
                continue
            self.assertIn(option_name, stored_db_options)
            self.assertEqual(option_value, stored_db_options[option_name])

        return

    def test_add_from_db_abspath(self):
        db_path = '/tmp/dbs/testdb'
        default_db_options = DatabaseOptions()
        status, content = self.handler.add(db_path)
        self.assertEqual(status, SUCCESS_STATUS)
        self.assertEqual(content, None)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertIn(db_path, store_datas)
        self.assertEqual(store_datas[db_path]['path'], os.path.join(self.dest, db_path))
        self.assertIsNotNone(store_datas[db_path]['uid'])
        stored_db_options = store_datas[db_path]['options']
        self.assertIsNotNone(stored_db_options)
        self.assertIsInstance(stored_db_options, dict)
        for option_name, option_value in default_db_options.iteritems():
            self.assertIn(option_name, stored_db_options)
            self.assertEqual(option_value, stored_db_options[option_name])

        return

    def test_add_from_db_relpath(self):
        db_path = './testdb'
        status, content = self.handler.add(db_path)
        self.assertEqual(status, FAILURE_STATUS)
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], DATABASE_ERROR)
        store_datas = json.load(open(self.handler.store, 'r'))
        self.assertNotIn(db_path, store_datas)

    def test_add_db_and_overflow_max_cache_size(self):
        orig_value = self.env['global']['max_cache_size']
        db_name = 'testdb'
        db_options = DatabaseOptions(block_cache_size=from_mo_to_bytes(1000))
        self.env['global']['max_cache_size'] = 32
        status, content = self.handler.add(db_name, db_options)
        self.assertEqual(status, FAILURE_STATUS)
        self.assertIsNotNone(content)
        self.assertIsInstance(content, list)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], DATABASE_ERROR)
        self.env['global']['max_cache_size'] = orig_value

    def test_add_db_with_enough_max_cache_size(self):
        db_name = 'testdb'
        db_options = DatabaseOptions(block_cache_size=from_mo_to_bytes(32))
        status, content = self.handler.add(db_name, db_options)
        self.assertEqual(status, SUCCESS_STATUS)

    def test_add_db_mounts_it_automatically(self):
        db_name = 'testdb'
        status, content = self.handler.add(db_name)
        db_uid = self.handler.index['name_to_uid'][db_name]
        self.assertEqual(self.handler[db_uid]['status'], self.handler.STATUSES.MOUNTED)
        self.assertIsNotNone(self.handler[db_uid]['connector'])
        self.assertIsInstance(self.handler[db_uid]['connector'], leveldb.LevelDB)

    def test_mount_unmounted_db(self):
        db_name = 'testdb'
        status, content = self.handler.add(db_name)
        db_uid = self.handler.index['name_to_uid'][db_name]
        self.handler[db_uid]['status'] = self.handler.STATUSES.UNMOUNTED
        self.handler[db_uid]['connector'] = None
        status, content = self.handler.mount(db_name)
        self.assertEqual(status, SUCCESS_STATUS)
        self.assertEqual(self.handler[db_uid]['status'], self.handler.STATUSES.MOUNTED)
        self.assertIsNotNone(self.handler[db_uid]['connector'])
        self.assertIsInstance(self.handler[db_uid]['connector'], leveldb.LevelDB)
        return

    def test_mount_already_mounted_db(self):
        db_name = 'testdb'
        status, content = self.handler.add(db_name)
        status, content = self.handler.mount(db_name)
        self.assertEqual(status, FAILURE_STATUS)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], DATABASE_ERROR)

    def test_mount_corrupted_db(self):
        db_name = 'testdb'
        status, content = self.handler.add(db_name)
        db_uid = self.handler.index['name_to_uid'][db_name]
        rm_from_pattern(self.handler[db_uid]['path'], 'MANIFEST*')
        status, content = self.handler.mount(db_name)
        self.assertEqual(status, FAILURE_STATUS)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], DATABASE_ERROR)

    def test_unmount_mounted_db(self):
        db_name = 'testdb'
        status, content = self.handler.add(db_name)
        db_uid = self.handler.index['name_to_uid'][db_name]
        status, content = self.handler.umount(db_name)
        self.assertEqual(status, SUCCESS_STATUS)
        self.assertEqual(self.handler[db_uid]['status'], self.handler.STATUSES.UNMOUNTED)
        self.assertIsNone(self.handler[db_uid]['connector'])

    def test_umount_already_unmounted_db(self):
        db_name = 'testdb'
        status, content = self.handler.add(db_name)
        db_uid = self.handler.index['name_to_uid'][db_name]
        self.handler[db_uid]['status'] = self.handler.STATUSES.UNMOUNTED
        self.handler[db_uid]['connector'] = None
        status, content = self.handler.umount(db_name)
        self.assertEqual(status, FAILURE_STATUS)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0], DATABASE_ERROR)
        return