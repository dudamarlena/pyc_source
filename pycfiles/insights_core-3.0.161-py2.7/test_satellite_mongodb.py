# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_satellite_mongodb.py
# Compiled at: 2020-03-25 13:10:41
import pytest, doctest
from insights.tests import context_wrap
from insights.parsers import SkipException, ParseException
from insights.parsers import satellite_mongodb
MONGO_PULP_STORAGE_ENGINE_OUTPUT1 = '\nMongoDB shell version v3.4.9\nconnecting to: mongodb://127.0.0.1:27017/pulp_database\nMongoDB server version: 3.4.9\n{\n        "name" : "wiredTiger",\n        "supportsCommittedReads" : true,\n        "readOnly" : false,\n        "persistent" : true\n}\n'
MONGO_PULP_STORAGE_ENGINE_OUTPUT2 = '\nMongoDB shell version v3.4.9\nconnecting to: mongodb://127.0.0.1:27017/pulp_database\nMongoDB server version: 3.4.9\n'
MONGO_PULP_STORAGE_ENGINE_OUTPUT3 = ("\nMongoDB shell version v3.4.9\nconnecting to: mongodb://127.0.0.1:27017/pulp_database\n2020-02-13T23:19:57.750-0500 W NETWORK  [thread1] Failed to connect to 127.0.0.1:27017, in(checking socket for error after poll), reason: Connection refused\n2020-02-13T23:19:57.751-0500 E QUERY    [thread1] Error: couldn't connect to server 127.0.0.1:27017, connection attempt failed :\nconnect@src/mongo/shell/mongo.js:237:13\n@(connect):1:6\nexception: connect failed\n").strip()
MONGO_PULP_STORAGE_ENGINE_OUTPUT4 = ('\nMongoDB shell version v3.4.9\nconnecting to: mongodb://127.0.0.1:27017/pulp_database\n{\n    "name" wrong data\n}\n').strip()

def test_doc_examples():
    output = satellite_mongodb.MongoDBStorageEngine(context_wrap(MONGO_PULP_STORAGE_ENGINE_OUTPUT1))
    globs = {'satellite_storage_engine': output}
    failed, tested = doctest.testmod(satellite_mongodb, globs=globs)
    assert failed == 0


def test_satellite():
    output = satellite_mongodb.MongoDBStorageEngine(context_wrap(MONGO_PULP_STORAGE_ENGINE_OUTPUT1))
    assert output['supportsCommittedReads'] == 'true'
    assert output['readOnly'] == 'false'
    assert output['persistent'] == 'true'


def test_no_storage_engine():
    with pytest.raises(SkipException):
        satellite_mongodb.MongoDBStorageEngine(context_wrap(MONGO_PULP_STORAGE_ENGINE_OUTPUT2))
    with pytest.raises(SkipException):
        satellite_mongodb.MongoDBStorageEngine(context_wrap(MONGO_PULP_STORAGE_ENGINE_OUTPUT3))
    with pytest.raises(ParseException):
        satellite_mongodb.MongoDBStorageEngine(context_wrap(MONGO_PULP_STORAGE_ENGINE_OUTPUT4))