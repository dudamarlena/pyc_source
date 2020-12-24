# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/src/nozama-cloudsearch/nozama-cloudsearch-data/nozama/cloudsearch/data/tests/conftest.py
# Compiled at: 2013-12-03 06:00:21
"""
"""
import logging, pytest

@pytest.fixture(scope='session')
def logger(request):
    """Set up a root logger showing all entries in the console.
    """
    log = logging.getLogger()
    hdlr = logging.StreamHandler()
    fmt = '%(asctime)s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt)
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    log.setLevel(logging.DEBUG)
    log.propagate = False
    return log


@pytest.fixture(scope='function')
def mongodb(request):
    """Set up a mongo connection reset and ready to roll.
    """
    from nozama.cloudsearch.data import db
    db.init(dict(db_name='unittesting-db'))
    db.db().hard_reset()


@pytest.fixture(scope='function')
def elastic(request):
    """Set up a elasticsearch connection reset and ready to roll.

    This will attempt to connect to the default elasticsearch instance
    on http://localhost:9200. Its not configurable yet.

    """
    from nozama.cloudsearch.data.db import init_es, get_es
    init_es(dict(es_namespace='ut_'))
    get_es().hard_reset()