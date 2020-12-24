# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_authorization.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 12701 bytes
import random, time, unittest
from okera import context
from okera._thrift_api import TRecordServiceException
from okera._thrift_api import TTypeId
TEST_DB = 'auth_test_db'
TEST_ROLE = 'auth_test_role'
TEST_USER = 'auth_test_user'

class AuthorizationTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Initializes one time state that is shared across test cases. This is used
            to speed up the tests. State that can be shared across (but still stable)
            should be here instead of __cleanup()."""
        super(AuthorizationTest, cls).setUpClass()

    @staticmethod
    def __ddl(conn, sql):
        print(sql)
        conn.execute_ddl(sql)

    def __cleanup(self, conn):
        """ Cleanups all the test state used in this test to "reset" the catalog.
            dbs can be specified to do the initialize over multiple databases.
            This can be used for tests that use multiple dbs (but makes the test
            take longer). By default, only load TEST_DB.
        """
        self._AuthorizationTest__ddl(conn, 'DROP ROLE IF EXISTS %s' % TEST_ROLE)
        self._AuthorizationTest__ddl(conn, 'CREATE ROLE %s' % TEST_ROLE)
        self._AuthorizationTest__ddl(conn, 'GRANT ROLE %s to GROUP %s' % (TEST_ROLE, TEST_USER))

    @staticmethod
    def __top_level_columns(schema):
        cols = schema.nested_cols
        if not cols:
            cols = schema.cols
        to_skip = 0
        result = []
        types = []
        for c in cols:
            if to_skip == 0:
                result.append(c.name)
                types.append(c.type)
            else:
                to_skip -= 1
            if c.type.num_children:
                to_skip += c.type.num_children

        return (
         result, types)

    @staticmethod
    def __collect_grant_objects(conn):
        grants = conn.execute_ddl('SHOW GRANT ROLE %s' % TEST_ROLE)
        result = []
        for grant in grants:
            path = ''
            if grant[1]:
                path = grant[1]
                if grant[2]:
                    path += '.' + grant[2]
                    if grant[3]:
                        path += '.' + grant[3]
                else:
                    path += '.*'
            else:
                path = '*'
            result.append(path)

        return result

    def test_revoke_db_no_cascade(self):
        ctx = context()
        with ctx.connect() as (conn):
            self._AuthorizationTest__cleanup(conn)
            conn.execute_ddl('GRANT SELECT ON DATABASE okera_sample TO ROLE %s' % TEST_ROLE)
            conn.execute_ddl('GRANT SELECT ON TABLE okera_sample.sample TO ROLE %s' % TEST_ROLE)
            conn.execute_ddl('GRANT SELECT(record) ON TABLE okera_sample.sample TO ROLE %s' % TEST_ROLE)
            objs = self._AuthorizationTest__collect_grant_objects(conn)
            print(objs)
            self.assertTrue('okera_sample.*' in objs)
            self.assertTrue('okera_sample.sample' in objs)
            self.assertTrue('okera_sample.sample.record' in objs)
            self.assertTrue(len(objs) == 3)
            conn.execute_ddl('REVOKE SELECT ON DATABASE okera_sample FROM ROLE %s' % TEST_ROLE)
            time.sleep(7)
            objs = self._AuthorizationTest__collect_grant_objects(conn)
            print(objs)
            self.assertTrue('okera_sample.sample' in objs)
            self.assertTrue('okera_sample.sample.record' in objs)
            self.assertTrue(len(objs) == 2)
            conn.execute_ddl('REVOKE SELECT ON TABLE okera_sample.sample FROM ROLE %s' % TEST_ROLE)
            time.sleep(7)
            objs = self._AuthorizationTest__collect_grant_objects(conn)
            print(objs)
            self.assertTrue('okera_sample.sample.record' in objs)
            self.assertTrue(len(objs) == 1)
            conn.execute_ddl('REVOKE SELECT(record) ON TABLE okera_sample.sample FROM ROLE %s' % TEST_ROLE)
            objs = self._AuthorizationTest__collect_grant_objects(conn)
            self.assertTrue(len(objs) == 0)

    def __test_dataset(self, ctx, conn, db, ds):
        ctx.disable_auth()
        schema = conn.plan('select * from %s.%s' % (db, ds)).schema
        cols, types = self._AuthorizationTest__top_level_columns(schema)
        self._AuthorizationTest__cleanup(conn)
        visible_cols = []
        print('Testing dataset: %s.%s...' % (db, ds))
        order = list(range(0, len(cols)))
        random.shuffle(order)
        for idx in range(0, len(cols)):
            c = cols[order[idx]]
            print('    granting to col: %s' % c)
            ctx.disable_auth()
            self._AuthorizationTest__ddl(conn, 'GRANT SELECT(%s) ON TABLE %s.%s TO ROLE %s' % (
             c, db, ds, TEST_ROLE))
            visible_cols.append(c)
            schema = conn.plan('select * from %s.%s' % (db, ds)).schema
            result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
            self.assertEqual(len(cols), len(result_cols))
            ctx.enable_token_auth(token_str=TEST_USER)
            schema = conn.plan('select * from %s.%s' % (db, ds)).schema
            result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
            self.assertEqual(len(visible_cols), len(result_cols))
            sql = 'SELECT * FROM (SELECT * FROM %s.%s)v' % (db, ds)
            schema = conn.plan(sql).schema
            result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
            self.assertEqual(len(visible_cols), len(result_cols))
            schema = conn.plan('select %s from %s.%s' % (
             ','.join(visible_cols), db, ds)).schema
            result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
            self.assertEqual(len(visible_cols), len(result_cols))
            sql = 'SELECT * FROM (SELECT %s FROM %s.%s)v' % (
             ','.join(visible_cols), db, ds)
            schema = conn.plan(sql).schema
            result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
            self.assertEqual(len(visible_cols), len(result_cols))
            sql = 'SELECT %s FROM (SELECT %s FROM %s.%s)v' % (
             ','.join(visible_cols), ','.join(visible_cols), db, ds)
            schema = conn.plan(sql).schema
            result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
            self.assertEqual(len(visible_cols), len(result_cols))
            if types[order[idx]].type_id == TTypeId.RECORD or types[order[idx]].type_id == TTypeId.ARRAY or types[order[idx]].type_id == TTypeId.MAP:
                with self.assertRaises(TRecordServiceException) as (ex_ctx):
                    conn.plan('SELECT %s FROM %s.%s WHERE %s IS NOT NULL' % (
                     visible_cols[0], db, ds, c))
                self.assertTrue('does not support complex types' in str(ex_ctx.exception))
            else:
                schema = conn.plan('SELECT %s FROM %s.%s WHERE %s IS NOT NULL' % (
                 visible_cols[0], db, ds, c)).schema
                result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
                self.assertEqual(1, len(result_cols))
            for i in range(idx + 1, len(cols)):
                with self.assertRaises(TRecordServiceException) as (ex_ctx):
                    conn.plan('select %s from %s.%s' % (cols[order[i]], db, ds))
                self.assertTrue('not have privilege' in str(ex_ctx.exception))
                with self.assertRaises(TRecordServiceException) as (ex_ctx):
                    conn.plan('select %s from %s.%s WHERE %s IS NOT NULL' % (
                     ','.join(visible_cols), db, ds, cols[order[i]]))
                self.assertTrue('not have privilege' in str(ex_ctx.exception))
                select_list = visible_cols.copy()
                select_list.append(cols[order[i]])
                for _ in range(0, 3):
                    random.shuffle(select_list)
                    with self.assertRaises(TRecordServiceException) as (ex_ctx):
                        conn.plan('select %s from %s.%s' % (
                         ','.join(select_list), db, ds))
                    self.assertTrue('not have privilege' in str(ex_ctx.exception))

                if types[i].type_id == TTypeId.RECORD:
                    with self.assertRaises(TRecordServiceException) as (ex_ctx):
                        conn.plan('select %s from %s.%s WHERE %s.f1 IS NOT NULL' % (
                         ','.join(visible_cols), db, ds, cols[order[i]]))
                    self.assertTrue('not have privilege' in str(ex_ctx.exception) or 'Could not resolve' in str(ex_ctx.exception))

        print('Entire table: ' + ds)
        ctx.disable_auth()
        conn.execute_ddl('GRANT SELECT ON TABLE %s.%s TO ROLE %s' % (
         db, ds, TEST_ROLE))
        self.assertTrue(len(visible_cols), len(cols))
        ctx.enable_token_auth(token_str=TEST_USER)
        schema = conn.plan('select * from %s.%s' % (db, ds)).schema
        result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
        self.assertEqual(len(cols), len(result_cols))
        schema = conn.plan('select %s from %s.%s' % (
         ','.join(visible_cols), db, ds)).schema
        result_cols, _ = self._AuthorizationTest__top_level_columns(schema)
        self.assertEqual(len(cols), len(result_cols))

    def test_complex_types(self):
        not_working = [
         'struct_nested_s1_s2']
        print('THESE ARE NOT WORKING: ' + str(not_working))
        slow = [
         'test_bucketing_tbl', 'zd1216', 'zd1216_with_subscriptionlimit']
        print('THESE ARE SLOW: ' + str(slow))
        ctx = context()
        with ctx.connect() as (conn):
            for ds in ['struct_t', 'struct_t2', 'struct_t3', 'struct_nested', 'struct_array_struct', 'struct_t_id', 'struct_nested_s1_f1',
             'struct_view', 'struct_t_view', 'struct_t_view2',
             'struct_t_s1', 'struct_nested_view', 'struct_nested_s1',
             'rs_complex_array_map_t', 'strarray_t', 'strarray_t_view',
             'array_struct_array', 'array_struct_t', 'array_t', 'avrotbl',
             'map_t', 'market_v20_single', 'market_v30_single',
             'multiple_structs_nested', 'users', 'user_phone_numbers',
             'user_phone_numbers_map', 'view_over_multiple_structs']:
                self._AuthorizationTest__test_dataset(ctx, conn, 'rs_complex', ds)


if __name__ == '__main__':
    unittest.main()