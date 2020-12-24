# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/tests/test_database_interface.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 4783 bytes
"""Tests for the ``database_interface.py`` module.

Authors
-------

    - Joe Filippazzo
    - Matthew Bourque

Use
---

    These tests can be run via the command line (omit the ``-s`` to
    suppress verbose output to stdout):
    ::

        pytest -s database_interface.py
"""
import datetime, os, pytest, random, string
from jwql.database import database_interface as di
from jwql.utils.constants import ANOMALIES
from jwql.utils.utils import get_config
ON_JENKINS = '/home/jenkins' in os.path.expanduser('~')

@pytest.mark.skipif(ON_JENKINS, reason='Requires access to development database server.')
def test_all_tables_exist():
    """Test that the table ORMs defined in ``database_interface``
    actually exist as tables in the database"""
    table_orms = []
    database_interface_attributes = di.__dict__.keys()
    for attribute in database_interface_attributes:
        table_object = getattr(di, attribute)
        try:
            table_orms.append(table_object.__tablename__)
        except AttributeError:
            pass

    existing_tables = di.engine.table_names()
    for table in table_orms:
        assert table in existing_tables


def test_anomaly_orm_factory():
    """Test that the ``anomaly_orm_factory`` function successfully
    creates an ORM and contains the appropriate columns"""
    test_table_name = 'test_anomaly_table'
    TestAnomalyTable = di.anomaly_orm_factory('test_anomaly_table')
    table_attributes = TestAnomalyTable.__dict__.keys()
    assert str(TestAnomalyTable) == "<class 'jwql.database.database_interface.{}'>".format(test_table_name)
    for anomaly in ANOMALIES:
        assert anomaly in table_attributes


@pytest.mark.skipif(ON_JENKINS, reason='Requires access to development database server.')
def test_anomaly_records():
    """Test to see that new records can be entered"""
    random_rootname = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(10))
    di.session.add(di.Anomaly(rootname=random_rootname, flag_date=(datetime.datetime.today()),
      user='test',
      ghost=True))
    di.session.commit()
    ghosts = di.session.query(di.Anomaly).filter(di.Anomaly.rootname == random_rootname).filter(di.Anomaly.ghost == 'True')
    assert ghosts.data_frame.iloc[0]['ghost'] == True


@pytest.mark.skipif(ON_JENKINS, reason='Requires access to development database server.')
def test_load_connections():
    """Test to see that a connection to the database can be
    established"""
    session, base, engine, meta = di.load_connection(get_config()['connection_string'])
    if not str(type(session)) == "<class 'sqlalchemy.orm.session.Session'>":
        raise AssertionError
    else:
        if not str(type(base)) == "<class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>":
            raise AssertionError
        elif not str(type(engine)) == "<class 'sqlalchemy.engine.base.Engine'>":
            raise AssertionError
        assert str(type(meta)) == "<class 'sqlalchemy.sql.schema.MetaData'>"


def test_monitor_orm_factory():
    """Test that the ``monitor_orm_factory`` function successfully
    creates an ORM and contains the appropriate columns"""
    test_table_name = 'instrument_test_monitor_table'
    test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'monitor_table_definitions', 'instrument')
    test_filename = os.path.join(test_dir, '{}.txt'.format(test_table_name))
    if not os.path.isdir(test_dir):
        os.mkdir(test_dir)
    else:
        with open(test_filename, 'w') as (f):
            f.write('TEST_COLUMN, string')
        TestMonitorTable = di.monitor_orm_factory(test_table_name)
        table_attributes = TestMonitorTable.__dict__.keys()
        assert str(TestMonitorTable) == "<class 'jwql.database.database_interface.{}'>".format(test_table_name)
    for column in ('id', 'entry_date', 'test_column'):
        assert column in table_attributes

    if os.path.isfile(test_filename):
        os.remove(test_filename)
    if os.path.isdir(test_dir):
        os.rmdir(test_dir)