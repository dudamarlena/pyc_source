# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/test_roles.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 6799 bytes
import unittest
from okera import context, _thrift_api
TEST_USER = 'roles_test_user'

def disable_auth(ctx, params):
    ctx.disable_auth()
    params.requesting_user = None


def enable_auth(ctx, params, user):
    ctx.enable_token_auth(token_str=user)
    params.requesting_user = user


def get_grantable_roles(conn, params):
    return conn._underlying_client().GetGrantableRoles(params)


class RolesTest(unittest.TestCase):

    def test_get_grantable_roles(self):
        ctx = context()
        with ctx.connect() as (conn):
            params = _thrift_api.TGetGrantableRolesParams()
            disable_auth(ctx, params)
            conn.execute_ddl('DROP ROLE IF EXISTS grantable_role')
            conn.execute_ddl('CREATE ROLE grantable_role')
            conn.execute_ddl('GRANT ROLE grantable_role to GROUP %s' % TEST_USER)
            disable_auth(ctx, params)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) > 0)
            self.assertTrue('grantable_role' in retrieved_roles)
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) == 0)
            disable_auth(ctx, params)
            conn.execute_ddl('\n            GRANT SELECT ON TABLE okera_sample.sample\n            TO ROLE grantable_role WITH GRANT OPTION')
            admin_roles = get_grantable_roles(conn, params).roles
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) == 0)
            params.database = 'okera_sample'
            params.table = 'sample'
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) > 0)
            self.assertEqual(admin_roles, retrieved_roles)
            params.database = 'okera_sample'
            params.table = 'users'
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) == 0)
            params.database = 'okera_sample'
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) == 0)
            disable_auth(ctx, params)
            conn.execute_ddl('\n            GRANT SELECT ON DATABASE okera_sample\n            TO ROLE grantable_role WITH GRANT OPTION')
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) > 0)
            self.assertEqual(admin_roles, retrieved_roles)
            params.database = 'okera_system'
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) == 0)
            disable_auth(ctx, params)
            conn.execute_ddl('\n            GRANT SELECT ON SERVER\n            TO ROLE grantable_role WITH GRANT OPTION')
            params.database = ''
            params.table = ''
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) > 0)
            self.assertEqual(admin_roles, retrieved_roles)
            params.database = 'okera_system'
            enable_auth(ctx, params, TEST_USER)
            response = get_grantable_roles(conn, params)
            retrieved_roles = response.roles
            self.assertTrue(len(retrieved_roles) > 0)
            self.assertEqual(admin_roles, retrieved_roles)


if __name__ == '__main__':
    unittest.main()