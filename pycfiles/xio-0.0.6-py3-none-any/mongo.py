# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/lib/db/handlers/mongo.py
# Compiled at: 2018-12-07 08:05:34
"""

"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId

class Database:

    def __init__(self, name, params):
        self.name = name.replace('.', '_')
        self.uri = params.get('uri')
        client = MongoClient(self.uri) if self.uri else MongoClient()
        self.db = client[name]

    def list(self):
        cols = self.db.collection_names()
        result = []
        for name in cols:
            collection = self.db[name]
            container = Container(name, collection)
            result.append(container)

        return result

    def get(self, name):
        collection = self.db[name]
        return Container(name, collection)

    def put(self, name):
        collection = self.db[name]
        newc = Container(name, collection)
        return newc

    def delete(self, name):
        self.db.drop_collection(name)


class Container:

    def __init__(self, name, collection):
        self.collection = collection
        self.name = name

    def exist(self, id):
        query = {'_id': id}
        row = self.collection.find_one(query)
        return bool(row)

    def get(self, id):
        query = {'_id': id}
        row = self.collection.find_one(query)
        return row

    def select(self, filter=None, fields=None, limit=None, start=0, sort=None, **kwargs):
        query = filter2query(filter)
        cursor = self.collection.find(query)
        if limit:
            cursor.skip(start)
            cursor.limit(limit)
        if sort:
            mongosort = []
            for s in sort:
                s = s.strip()
                orient = ASCENDING
                if s.split(' ').pop() == 'desc':
                    orient = DESCENDING
                    s = s.split(' ').pop(0)
                mongosort.append((s, orient))

            cursor.sort(mongosort)
        from bson.json_util import dumps
        result = []
        for row in cursor:
            result.append(row)

        return result

    def post(self, data):
        return self.collection.insert(data)

    def put(self, index, data):
        query = {'_id': index}
        data = data or {}
        self.delete(index)
        return self.collection.update(query, {'$set': data}, upsert=True)

    def update(self, index, data, *args, **kwargs):
        query = {'_id': index}
        assert '_id' in data and data.pop('_id') == index
        return self.collection.update(query, {'$set': data}, upsert=False)

    def truncate(self):
        return self.collection.remove({})

    def delete(self, index=None, filter=None):
        if index:
            query = {'_id': index}
        else:
            if filter:
                query = filter2query(filter)
            else:
                query = {}
            if query:
                return self.collection.remove(query)

    def count(self, filter=None):
        query = filter2query(filter)
        cursor = self.collection.find(query)
        return cursor.count()


def filter2query(filter):
    """
    http://docs.mongodb.org/manual/reference/operator/query/
    """
    query = {}
    filter = filter or {}
    for k, v in filter.items():
        if isinstance(v, tuple):
            operator, v = v
            mop = '$%s' % operator
            value = {mop: v}
        elif isinstance(v, list):
            value = {'$in': v}
        else:
            value = v
        query[k] = value

    return query