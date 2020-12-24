# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_ddl.py
# Compiled at: 2016-02-12 12:18:44
import os
from nose.tools import ok_
from dmsa import ddl
SERVICE = os.environ.get('DMSA_TEST_SERVICE', 'http://data-models.origins.link/')

def test_all():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', service=SERVICE)
    ok_(ddl_output)


def test_drop_all():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', drop=True, service=SERVICE)
    ok_(ddl_output)


def test_notables():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', tables=False, service=SERVICE)
    ok_(ddl_output)


def test_drop_notables():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', tables=False, drop=True, service=SERVICE)
    ok_(ddl_output)


def test_noconstraints():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', constraints=False, service=SERVICE)
    ok_(ddl_output)


def test_drop_noconstraints():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', constraints=False, drop=True, service=SERVICE)
    ok_(ddl_output)


def test_noindexes():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', indexes=False, service=SERVICE)
    ok_(ddl_output)


def test_drop_noindexes():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', indexes=False, drop=True, service=SERVICE)
    ok_(ddl_output)


def test_delete():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', delete_data=True)
    ok_(ddl_output)


def test_logging_all():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', logging=True)
    ok_(ddl_output)


def test_nologging_all():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', nologging=True)
    ok_(ddl_output)


def test_logging_notables():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', logging=True, tables=False)
    ok_(ddl_output)


def test_nologging_notables():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', nologging=True, tables=False)
    ok_(ddl_output)


def test_logging_noindexes():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', logging=True, indexes=False)
    ok_(ddl_output)


def test_nologging_noindexes():
    ddl_output = ddl.generate('omop', '5.0.0', 'sqlite', nologging=True, indexes=False)
    ok_(ddl_output)