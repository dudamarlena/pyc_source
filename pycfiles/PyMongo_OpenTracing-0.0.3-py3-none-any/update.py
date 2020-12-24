# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pymongo_mate/crud/update.py
# Compiled at: 2017-10-12 14:36:33
__doc__ = '\nextend ``pymongo.Collection.update`` method.\n'
__all__ = [
 'upsert_many']

def upsert_many(col, data):
    u"""
    Only used when having "_id" field.

    **中文文档**

    要求 ``data`` 中的每一个 ``document`` 都必须有 ``_id`` 项。这样才能进行
    ``upsert`` 操作。
    """
    ready_to_insert = list()
    for doc in data:
        res = col.update({'_id': doc['_id']}, {'$set': doc}, upsert=False)
        if res['nModified'] == 0 and res['updatedExisting'] is False:
            ready_to_insert.append(doc)

    col.insert(ready_to_insert)