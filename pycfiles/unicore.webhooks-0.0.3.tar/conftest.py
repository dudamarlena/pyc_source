# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.webhooks/unicore/webhooks/conftest.py
# Compiled at: 2016-06-21 11:57:16
import os, pytest
from pyramid.paster import get_appsettings, setup_logging
from sqlalchemy import engine_from_config
from unicore.webhooks.models import DBSession, Base

def pytest_addoption(parser):
    parser.addoption('--ini', action='store', metavar='INI_FILE', default='test.ini', help='use INI_FILE to configure SQLAlchemy')


@pytest.fixture(scope='session')
def appsettings(request):
    config_uri = os.path.abspath(request.config.option.ini)
    setup_logging(config_uri)
    return get_appsettings(config_uri)


@pytest.fixture(scope='session')
def sqlengine(request, appsettings):
    engine = engine_from_config(appsettings, 'sqlalchemy.')
    DBSession.configure(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection, expire_on_commit=False)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection