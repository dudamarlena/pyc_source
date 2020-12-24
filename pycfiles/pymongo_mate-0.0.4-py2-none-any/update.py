# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pymongo_mate/crud/update.py
# Compiled at: 2017-10-12 14:36:33
"""
extend ``pymongo.Collection.update`` method.
"""
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