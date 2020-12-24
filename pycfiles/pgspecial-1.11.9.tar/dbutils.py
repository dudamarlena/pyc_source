# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/irina/src/pgspecial/tests/dbutils.py
# Compiled at: 2017-10-27 12:23:29
import pytest, psycopg2, psycopg2.extras
POSTGRES_USER, POSTGRES_HOST = ('postgres', 'localhost')

def db_connection(dbname=None):
    conn = psycopg2.connect(user=POSTGRES_USER, host=POSTGRES_HOST, database=dbname)
    conn.autocommit = True
    return conn


try:
    conn = db_connection()
    CAN_CONNECT_TO_DB = True
    SERVER_VERSION = conn.server_version
except:
    CAN_CONNECT_TO_DB = False
    SERVER_VERSION = 0

dbtest = pytest.mark.skipif(not CAN_CONNECT_TO_DB, reason="Need a postgres instance at localhost accessible by user '%s'" % POSTGRES_USER)

def create_db(dbname):
    with db_connection().cursor() as (cur):
        try:
            cur.execute('CREATE DATABASE _test_db')
        except:
            pass


def setup_db(conn):
    with conn.cursor() as (cur):
        cur.execute('create schema schema1')
        cur.execute('create schema schema2')
        cur.execute('create table tbl1(id1 integer, txt1 text, CONSTRAINT id_text PRIMARY KEY(id1, txt1))')
        cur.execute('create table tbl2(id2 serial, txt2 text)')
        cur.execute('create table schema1.s1_tbl1(id1 integer, txt1 text)')
        cur.execute('create table tbl3(c3 circle, exclude using gist (c3 with &&))')
        cur.execute('create table "Inh1"(value1 integer) inherits (tbl1)')
        cur.execute('create table inh2(value2 integer) inherits (tbl1, tbl2)')
        cur.execute('create view vw1 as select * from tbl1')
        cur.execute('create view schema1.s1_vw1 as\n                       select * from schema1.s1_tbl1')
        cur.execute('create materialized view mvw1 as select * from tbl1')
        cur.execute('create materialized view schema1.s1_mvw1 as\n                       select * from schema1.s1_tbl1')
        cur.execute('create type foo AS (a int, b text)')
        cur.execute('create function func1() returns int language sql as\n                       $$select 1$$')
        cur.execute('create function schema1.s1_func1() returns int language\n                       sql as $$select 2$$')


def teardown_db(conn):
    with conn.cursor() as (cur):
        cur.execute('\n            DROP SCHEMA public CASCADE;\n            CREATE SCHEMA public;\n            DROP SCHEMA IF EXISTS schema1 CASCADE;\n            DROP SCHEMA IF EXISTS schema2 CASCADE')