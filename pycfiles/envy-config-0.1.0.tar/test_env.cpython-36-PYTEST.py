# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jerluc/dev/src/github.com/stationa/envy/tests/test_env.py
# Compiled at: 2018-02-09 20:12:12
# Size of source mod 2**32: 1622 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from envy import Env

class SingleLevelEnv(Env):
    a = 'HELLO'
    b = 123
    c = False


def test_single_level_env_defaults():
    env = SingleLevelEnv('TEST', env={})
    @py_assert1 = env.a
    @py_assert5 = SingleLevelEnv.a
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py6)s\n{%(py6)s = %(py4)s.a\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(SingleLevelEnv) if 'SingleLevelEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SingleLevelEnv) else 'SingleLevelEnv',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = env.b
    @py_assert5 = SingleLevelEnv.b
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.b\n} == %(py6)s\n{%(py6)s = %(py4)s.b\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(SingleLevelEnv) if 'SingleLevelEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SingleLevelEnv) else 'SingleLevelEnv',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = env.c
    @py_assert5 = SingleLevelEnv.c
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.c\n} == %(py6)s\n{%(py6)s = %(py4)s.c\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(SingleLevelEnv) if 'SingleLevelEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SingleLevelEnv) else 'SingleLevelEnv',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_single_level_env_overrides():
    new_a = 'GOODBYE'
    new_b = '321'
    new_c = 'True'
    env = SingleLevelEnv('TEST', env={'TEST_A':new_a, 
     'TEST_B':new_b, 
     'TEST_C':new_c})
    @py_assert1 = env.a
    @py_assert3 = @py_assert1 == new_a
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.a\n} == %(py4)s', ), (@py_assert1, new_a)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(new_a) if 'new_a' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_a) else 'new_a'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = env.b
    @py_assert6 = int(new_b)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.b\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py5':@pytest_ar._saferepr(new_b) if 'new_b' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_b) else 'new_b',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = env.c
    @py_assert6 = bool(new_c)
    @py_assert3 = @py_assert1 == @py_assert6
    if not @py_assert3:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.c\n} == %(py7)s\n{%(py7)s = %(py4)s(%(py5)s)\n}', ), (@py_assert1, @py_assert6)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(bool) if 'bool' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bool) else 'bool',  'py5':@pytest_ar._saferepr(new_c) if 'new_c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_c) else 'new_c',  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert6 = None


class DBEnv(Env):
    connection_string = 'postgres://un:pw@host:port/db'
    connection_timeout = 30


class AppEnv(Env):
    name = 'my-app'
    database = DBEnv


def test_multi_level_env_defaults():
    env = AppEnv('App', env={})
    @py_assert1 = env.name
    @py_assert5 = AppEnv.name
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py6)s\n{%(py6)s = %(py4)s.name\n}', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(AppEnv) if 'AppEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(AppEnv) else 'AppEnv',  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert2 = env.database
    @py_assert5 = isinstance(@py_assert2, DBEnv)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.database\n}, %(py4)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(DBEnv) if 'DBEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DBEnv) else 'DBEnv',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert5 = None
    @py_assert1 = env.database
    @py_assert3 = @py_assert1.connection_string
    @py_assert7 = DBEnv.connection_string
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.database\n}.connection_string\n} == %(py8)s\n{%(py8)s = %(py6)s.connection_string\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(DBEnv) if 'DBEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DBEnv) else 'DBEnv',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = env.database
    @py_assert3 = @py_assert1.connection_timeout
    @py_assert7 = DBEnv.connection_timeout
    @py_assert5 = @py_assert3 == @py_assert7
    if not @py_assert5:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.database\n}.connection_timeout\n} == %(py8)s\n{%(py8)s = %(py6)s.connection_timeout\n}', ), (@py_assert3, @py_assert7)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(DBEnv) if 'DBEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DBEnv) else 'DBEnv',  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_multi_level_env_overrides():
    new_name = 'db-service'
    new_connection_string = 'mysql://un:pw@host:port/db'
    new_connection_timeout = '45'
    env = AppEnv('APP', env={'APP_NAME':new_name, 
     'APP_DATABASE_CONNECTION_STRING':new_connection_string, 
     'APP_DATABASE_CONNECTION_TIMEOUT':new_connection_timeout})
    @py_assert1 = env.name
    @py_assert3 = @py_assert1 == new_name
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py4)s', ), (@py_assert1, new_name)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(new_name) if 'new_name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_name) else 'new_name'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert2 = env.database
    @py_assert5 = isinstance(@py_assert2, DBEnv)
    if not @py_assert5:
        @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.database\n}, %(py4)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(DBEnv) if 'DBEnv' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(DBEnv) else 'DBEnv',  'py6':@pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert2 = @py_assert5 = None
    @py_assert1 = env.database
    @py_assert3 = @py_assert1.connection_string
    @py_assert5 = @py_assert3 == new_connection_string
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.database\n}.connection_string\n} == %(py6)s', ), (@py_assert3, new_connection_string)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(new_connection_string) if 'new_connection_string' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_connection_string) else 'new_connection_string'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = env.database
    @py_assert3 = @py_assert1.connection_timeout
    @py_assert8 = int(new_connection_timeout)
    @py_assert5 = @py_assert3 == @py_assert8
    if not @py_assert5:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.database\n}.connection_timeout\n} == %(py9)s\n{%(py9)s = %(py6)s(%(py7)s)\n}', ), (@py_assert3, @py_assert8)) % {'py0':@pytest_ar._saferepr(env) if 'env' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(env) else 'env',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(int) if 'int' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(int) else 'int',  'py7':@pytest_ar._saferepr(new_connection_timeout) if 'new_connection_timeout' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_connection_timeout) else 'new_connection_timeout',  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = None