# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_aql.py
# Compiled at: 2013-04-13 11:48:16
# Size of source mod 2**32: 8522 bytes
import re
from .tests_base import TestsBase
from arango.aql import AQLQuery, F, V
from nose.tools import assert_equal

def CLEANUP(s):
    """
    Normalize spaces in queries
    """
    REPLACEMENTS = (('\\(\\s*', '('), ('\\s*\\)', ')'), ('\\s*([\\{\\}])\\s*', '\\1'),
                    ('\\s+', ' '))
    for ex, rpl in REPLACEMENTS:
        s = re.sub(ex, rpl, s, flags=re.S | re.M)

    return s.strip()


class TestAqlGeneration(TestsBase):

    def test_simple(self):
        q = AQLQuery(collection='user', no_cache=True)
        assert_equal(CLEANUP(q.build_query()), 'FOR obj IN user RETURN obj')
        assert_equal(CLEANUP(q.over('user').build_query()), 'FOR obj IN user RETURN obj')
        assert_equal(CLEANUP(q.iter('u').over('user').build_query()), 'FOR u IN user RETURN u')
        assert_equal(CLEANUP(q.iter('usr').over('user').build_query()), 'FOR usr IN user RETURN usr')
        assert_equal(CLEANUP(q.iter('usr').over('user').result('usr').build_query()), 'FOR usr IN user RETURN usr')

    def test_field_names(self):
        q1 = AQLQuery()
        q1.iter('user').over('users').result(fields={'user-first-name': 'user.first_name', 
         'user-last-name': 'user.last_name', 
         'user*age': "user['*age']"})
        assert_equal(CLEANUP(q1.build_query()), CLEANUP('\n                FOR user IN users RETURN\n                    {"user*age": user[\'*age\'],\n                    "user-first-name": user.first_name,\n                    "user-last-name": user.last_name\n                    }\n            '))

    def test_nested_queries(self):
        q1 = AQLQuery(collection='user')
        q2 = AQLQuery(collection='membership')
        assert_equal(CLEANUP(q1.nested(q2).result(user='obj', member='obj1').build_query()), CLEANUP('\n                FOR obj IN user\n                    FOR obj1 IN membership\n                RETURN {"member": obj1, "user": obj}\n            '))

    def test_sub_queries_in_return(self):
        q1 = AQLQuery(collection='user')
        q2 = AQLQuery(collection='membership')
        assert_equal(CLEANUP(q1.result(user='obj', members=F.LENGTH(q2)).build_query()), CLEANUP('\n                FOR obj IN user\n                RETURN {"members": LENGTH(\n                            FOR obj IN membership RETURN obj ),\n                        "user": obj}\n            '))

    def test_let_expr(self):
        q = AQLQuery(collection='user')
        q.let('name', 'u.first_name').let('email', F.LENGTH('u.email')).result(name='name', email='email')
        assert_equal(CLEANUP(q.build_query()), CLEANUP('\n                FOR obj IN user\n                    LET name = u.first_name\n                    LET email = LENGTH(u.email)\n                RETURN {"email": email, "name": name}\n            '))

    def test_let_subquery_expr(self):
        m = AQLQuery(collection='memberships')
        c = AQLQuery(collection='memberships')
        q = AQLQuery(collection='user')
        q.let('membership', m.iter('m1').result(within='m1.within', count=F.LENGTH(c.iter('m').result(groups='m.groups')))).result(name='obj.name', email='obj.email')
        assert_equal(CLEANUP(q.build_query()), CLEANUP('\n                FOR obj IN user\n                    LET membership = (\n                        FOR m1 IN memberships\n                        RETURN {"count": LENGTH(\n                                FOR m IN memberships\n                                RETURN\n                                {"groups": m.groups} ),\n                         "within": m1.within} )\n                RETURN {"email": obj.email, "name": obj.name}\n            '))

    def test_filter_expr(self):
        q = AQLQuery(collection='user')
        q.iter('u').filter("u.age >= 18 && u.name != ''").filter('u.email.length > 10').result(name='u.name', email='email')
        assert_equal(CLEANUP(q.build_query()), CLEANUP('\n                FOR u IN user\n                FILTER u.age >= 18 && u.name != \'\'\n                FILTER u.email.length > 10\n                RETURN {"email": email, "name": u.name}\n            '))

    def test_collect_expr(self):
        q1 = AQLQuery(collection='user')
        q2 = AQLQuery(collection='user')
        q3 = AQLQuery(collection='user')
        q1.iter('u').collect('emails', 'u.email').result(u='u', emails='emails')
        assert_equal(CLEANUP(q1.build_query()), CLEANUP('\n                FOR u IN user\n                COLLECT emails = u.email\n                RETURN {"emails": emails, "u": u}\n            '))
        q2.iter('u').collect('emails', 'u.email', into='g').result(u='u', g='g')
        assert_equal(CLEANUP(q2.build_query()), CLEANUP('\n                FOR u IN user\n                COLLECT emails = u.email INTO g\n                RETURN {"g": g, "u": u}\n            '))
        sq = AQLQuery(collection='members')
        q3.iter('u').collect('emails', 'u.email', into='g').result(u='u', g=F.MAX(sq.iter('c').over('g')))
        assert_equal(CLEANUP(q3.build_query()), CLEANUP('\n                FOR u IN user\n                COLLECT emails = u.email INTO g\n                RETURN {\n                    "g": MAX(\n                        FOR c IN g RETURN c\n                    ),\n                    "u": u\n                }\n            '))

    def test_sort(self):
        q = AQLQuery(collection='user')
        q.iter('u').sort('u.email DESC', 'u.name')
        assert_equal(CLEANUP(q.build_query()), CLEANUP('\n                FOR u IN user\n                SORT u.email DESC, u.name\n                RETURN u\n            '))

    def test_limit(self):
        q = AQLQuery(collection='user')
        q.iter('u').limit(10)
        assert_equal(CLEANUP(q.build_query()), CLEANUP('\n                FOR u IN user\n                LIMIT 10\n                RETURN u\n            '))
        q = AQLQuery(collection='user')
        q.iter('u').limit(10, offset=100)
        assert_equal(CLEANUP(q.build_query()), CLEANUP('\n                FOR u IN user\n                LIMIT 100, 10\n                RETURN u\n            '))

    def test_function_factory(self):
        assert_equal(F.LENGTH('a').build_query(), 'LENGTH(a)')
        assert_equal(F.PATH('a', 'b', 'c').build_query(), 'PATH(a, b, c)')
        assert_equal(CLEANUP(F.PATH('a', 'b', 'c').build_query()), 'PATH(a, b, c)')
        assert_equal(CLEANUP(F.PATH('a', 'b', 'c').build_query()), CLEANUP(F.PATH(V('a'), V('b'), V('c')).build_query()))
        assert_equal(CLEANUP(F.MERGE({'user1': {'name': 'J'}}, {'user2': {'name': 'T'}}).build_query()), CLEANUP('\n                MERGE(\n                    {"user1": {"name": "J"}},\n                    {"user2": {"name": "T"}})\n            '))
        assert_equal(CLEANUP(F.MERGE({'user1': {'name': V('u.name')}}, {'user2': {'name': 'T'}}).build_query()), CLEANUP('\n                MERGE(\n                    {"user1": {"name": u.name}},\n                    {"user2": {"name": "T"}})\n            '))

    def test_bind(self):
        q = AQLQuery(collection='user')
        assert_equal(q.bind(**{'data': 'test'}).execute().bindVars, {'data': 'test'})

    def test_cursor_args(self):
        q = AQLQuery(collection='user')
        assert_equal(q.cursor(batchSize=1).execute().batchSize, 1)