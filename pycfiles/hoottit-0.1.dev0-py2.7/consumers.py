# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/hoottit/consumers.py
# Compiled at: 2017-08-09 19:45:10
"""Similarly to the producers module, the consumers module exposes functions
that return generators. Differently to the producers module, these generators
consume (process) data, instead of creating it. Some people also call these
'coroutines', altough this term has been surrounded by confusion within the
Python community.
"""
import logging, time, hoottit.util

@hoottit.util.send_null_once
def mongo_upsert(collection, key, threshold):
    """Recieve objects to upsert to a MongoDB collection, based on key

    This function returns a generator that waits for data to be sent to it. For
    each object that it recieves, it executes and upsert operation in
    collection based on key. Basically, for an object a, if a document with
    key equal to a[key] already exists in the collection, it is replaced by a,
    otherwise a is inserted into the collection.
    """
    counter = 0
    begin = time.time()
    while True:
        obj = yield
        collection.update_one({key: obj[key]}, {'$set': obj}, upsert=True)
        logging.debug('Upserted object %s=%s', key, obj[key])
        counter += 1
        if counter % threshold == 0:
            minutes = (time.time() - begin) / 60.0
            docs_per_min = int(counter / minutes)
            logging.info('Upserted %d documents to %s with an average of %d docs/min.', counter, collection.name, docs_per_min)