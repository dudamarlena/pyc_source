# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/tests/test_cyclic.py
# Compiled at: 2015-02-12 15:25:14
import time, inspect, sys, pickle, os, numpy, pytest, random, shutil, pandas
from cStringIO import StringIO
import bayesdb.utils as utils
from bayesdb.client import Client
from bayesdb.engine import Engine
import bayesdb.bql_grammar as bql
test_tablenames = None
client = None
test_filenames = None

def setup_function(function):
    global client
    global test_filenames
    global test_tablenames
    test_tablenames = []
    test_filenames = []
    client = Client(testing=True)


def teardown_function(function):
    for test_tablename in test_tablenames:
        client.engine.drop_btable(test_tablename)

    for test_filename in test_filenames:
        if os.path.exists(test_filename):
            os.remove(test_filename)


def update_cyclic_schema(tablename):
    for col in range(10):
        client('update schema for %s set col_%i=cyclic(0, 6.284)' % (tablename, col), debug=True, pretty=False)


def create_cyclic(path='data/cyclic_test.csv', key_column=0):
    test_tablename = 'cyclictest' + str(int(time.time() * 1000000)) + str(int(random.random() * 10000000))
    csv_file_contents = open(path, 'r').read()
    client('create btable %s from %s' % (test_tablename, path), debug=True, pretty=False, key_column=key_column)
    test_tablenames.append(test_tablename)
    return test_tablename


def test_cyclic_initalize():
    """test a few functions with cyclic data"""
    test_tablename = create_cyclic(key_column=0)
    update_cyclic_schema(test_tablename)
    models = 3
    out = client('initialize %d models for %s' % (models, test_tablename), debug=True, pretty=False)[0]


def test_cyclic_all_the_things():
    """test a few functions with cyclic data"""
    test_tablename = create_cyclic(key_column=0)
    update_cyclic_schema(test_tablename)
    models = 3
    out = client('initialize %d models for %s' % (models, test_tablename), debug=True, pretty=False)[0]
    iterations = 2
    client('analyze %s for %i iterations wait' % (test_tablename, iterations), debug=True, pretty=False)
    out = client('select col_0 from %s' % test_tablename, pretty=False)[0]
    client('select predictive robability of col_0 from %s LIMIT 10' % test_tablename, pretty=False)
    client('simulate col_0 from %s times 100' % test_tablename, pretty=False)
    client('simulate col_0 GIVEN col_1 = 3.14 from %s times 100' % test_tablename, pretty=False)