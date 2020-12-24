# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_store.py
# Compiled at: 2010-05-12 10:25:54
import time, os
from shove import *
from khan.utils.testing import *
from khan.store import *
from khan.json import *
from khan.schema import *
from shove import BaseStore
from tempfile import mktemp

class CacheStoreTester(DictTester, TestCase):

    def setUp(self):
        self.store = CacheStore.create()
        super(CacheStoreTester, self).setUp()


class TestINIStore(TestCase):
    content = '\n        [groups]\n        admins = adminhere\n        developers = rms linus\n        trolls = sballmer\n        \n        [permissions]\n        see-site = trolls\n        edit-site = admins developers\n        commit = developers\n        \n        [test]\n        a = 1\n        \n        [[test1]]\n        b = 2\n        '

    def setUp(self):
        inifile = mktemp()
        with open(inifile, 'w') as (f):
            f.write(self.content)
        self.store = INIStore(inifile)
        self.inifile = inifile

    def tearDown(self):
        os.remove(self.inifile)

    def test_with_shove(self):
        store = self.store
        self.assertEqual(store['test']['test1']['b'], '2', 'read file failed')
        store['groups']['new_section'] = {'new_item': 'new_item_value'}
        self.assertEqual(store['groups']['new_section']['new_item'], 'new_item_value', 'value not save into file')
        store['groups']['admins'] = 'adminchanged'
        with open(self.inifile, 'r') as (f):
            context = f.read()
            self.assertTrue('adminchanged' in context, 'value not save into file')
            self.assertTrue('new_item_value' in context, 'value not save into file')


class ExpireStoreTester(DictTester, TestCase):

    def setUp(self):
        self.dbfile = mktemp()
        self.expires = 2
        self.store = ExpireStore(get_backend('khan.dbm://%s' % self.dbfile), expires=self.expires)
        super(ExpireStoreTester, self).setUp()

    def tearDown(self):
        os.unlink(self.dbfile)

    def test_expires(self):
        self.store['a'] = 1
        time.sleep(self.expires + 1)
        assert 'a' not in self.store


class TestRPCStore(BaseStore):

    def __init__(self, rpc_service_app):
        super(TestRPCStore, self).__init__('testrpcstore://')
        self.test_app = TestApp(rpc_service_app)

    def __getitem__(self, key):
        req_data = JSONRPCBuilder.request('store.get', key)
        resp = self.test_app.post('/', req_data)
        resp_data = jsonrpc_loads(resp.body)
        if resp_data['error']:
            raise KeyError('%s' % key)
        else:
            value = resp_data['result']
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            return self.loads(value)

    def __setitem__(self, key, value):
        req_data = JSONRPCBuilder.request('store.set', [key, self.dumps(value)])
        resp = self.test_app.post('/', req_data)

    def __delitem__(self, key):
        req_data = JSONRPCBuilder.request('store.remove', key)
        resp = self.test_app.post('/', req_data)

    def keys(self):
        req_data = JSONRPCBuilder.request('store.keys')
        resp = self.test_app.post('/', req_data)
        resp_data = jsonrpc_loads(resp.body)
        return resp_data['result']

    def __contains__(self, key):
        req_data = JSONRPCBuilder.request('store.has_key', key)
        resp = self.test_app.post('/', req_data)
        resp_data = jsonrpc_loads(resp.body)
        return resp_data['result']


class TestRPCStoreService(TestCase):

    def setUp(self):
        self.db_file = mktemp()
        self.store = get_backend('khan.dbm://%s' % self.db_file)
        self.app = RPCStoreService(self.store)
        self.test_app = TestApp(self.app)

    def tearDown(self):
        os.remove(self.db_file)

    def test(self):
        store = TestRPCStore(self.app)
        assert_dict(store)


if __name__ == '__main__':
    unittest.main()