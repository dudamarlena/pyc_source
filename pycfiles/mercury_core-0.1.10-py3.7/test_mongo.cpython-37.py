# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/common/unit/test_mongo.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 2626 bytes
import mock, pymongo, pytest
from mercury.common import mongo
from tests.common.unit.base import MercuryCommonUnitTest

@mock.patch('pymongo.MongoClient')
def test_get_connection(mock_mongo_client):
    """Test get_connection() creates a new MongoClient."""
    mongo.get_connection('host1')
    mock_mongo_client.assert_called_with(['host1'], replicaset=None)
    mongo.get_connection(['host1', 'host2'], replica_set='replica_set_name')
    mock_mongo_client.assert_called_with(['host1', 'host2'], replicaset='replica_set_name')


class MongoCollectionUnitTest(MercuryCommonUnitTest):

    def test___init__(self):
        """Test creation of MongoCollection."""
        collection = mongo.MongoCollection('db_name', 'collection_name')
        assert isinstance(collection.db, pymongo.database.Database)
        assert collection.db.name == 'db_name'
        assert isinstance(collection.collection, pymongo.collection.Collection)
        assert collection.collection.full_name == 'db_name.collection_name'

    def test___init__invalid_names(self):
        """Test creation of MongoCollection with invalid names."""
        with pytest.raises(pymongo.errors.InvalidName) as (exc):
            collection = mongo.MongoCollection('', 'collection_name')
        with pytest.raises(pymongo.errors.InvalidName):
            collection = mongo.MongoCollection('db_name', '')


def test_get_collection():
    """Test get_collection()"""
    collection = mongo.get_collection('db_name', 'collection_name')
    assert isinstance(collection, pymongo.collection.Collection)
    assert collection.full_name == 'db_name.collection_name'


def test_get_collection_invalid_names():
    """Test get_collection() with invalid names."""
    with pytest.raises(pymongo.errors.InvalidName):
        collection = mongo.get_collection('', 'collection_name')
    with pytest.raises(pymongo.errors.InvalidName):
        collection = mongo.get_collection('db_name', '')