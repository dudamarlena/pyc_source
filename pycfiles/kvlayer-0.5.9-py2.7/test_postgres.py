# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/tests/test_postgres.py
# Compiled at: 2015-07-31 13:31:44
import pytest, logging
logger = logging.getLogger(__name__)
config_postgres = {'namespace': 'test', 
   'storage_addresses': [
                       'host=test-postgres.diffeo.com port=5432 user=test dbname=test password=test']}
try:
    from kvlayer._postgres import PGStorage, _valid_namespace
    postgres_missing = 'False'
except ImportError:
    postgres_missing = 'True'

@pytest.mark.skipif(postgres_missing)
@pytest.mark.parametrize('badnamespace', [
 None,
 '9isnotaletter',
 '$isnotaletter'])
def test_illegal_namespaces(badnamespace):
    with pytest.raises(Exception):
        config = dict(config_postgres)
        config['namespace'] = badnamespace
        pg = PGStorage(config)


@pytest.mark.skipif(postgres_missing)
@pytest.mark.parametrize('namespace', [
 '_ok', 'Aok', 'aok'])
def test_legal_namespaces(namespace):
    assert _valid_namespace(namespace)