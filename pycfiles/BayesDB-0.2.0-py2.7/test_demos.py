# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/tests/test_demos.py
# Compiled at: 2015-02-12 15:25:14
import os, sys, pytest
from bayesdb.client import Client

def teardown_function(function):
    for fname in os.listdir('.'):
        if fname[(-4)] == '.png':
            os.remove(fname)


def run_example(name):
    client = Client(testing=True)
    file_path = os.path.join('../../examples/%s/%s_analysis.bql' % (name, name))
    results = client(open(file_path, 'r'), yes=True, pretty=False, plots=False, key_column=0)
    for r in results:
        if 'Error' in r or 'error' in r and r['error']:
            raise Exception(str(r))


def test_dha_example():
    run_example('dha')


def test_gss_example():
    run_example('gss')


def test_chicago_small_example():
    run_example('chicago_small')


def test_flights_example():
    run_example('flights')


def test_kiva_example():
    run_example('kiva')


def test_employees_example():
    run_example('employees')