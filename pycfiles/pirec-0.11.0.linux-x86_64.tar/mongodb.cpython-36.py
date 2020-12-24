# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/recorders/mongodb.py
# Compiled at: 2017-02-10 11:03:57
# Size of source mod 2**32: 1026 bytes
"""Exposes the MongoDB recorder class."""
try:
    from pymongo import MongoClient
except ImportError:
    pass

class MongoDB(object):
    __doc__ = 'Records results to a MongoDB database.\n\n    Args:\n        uri (str): MongoDB server URI e.g. ``mongodb://localhost:27017``\n        database (str): database name\n        collection (str): collection name\n\n    Note:\n        Use of this class requires the installation of the `pymongo\n        module <https://pypi.python.org/pypi/pymongo>`_.\n\n    See Also:\n        `MongoDB tutorial <https://api.mongodb.org/python/current/tutorial.html>`_\n    '

    def __init__(self, uri, database, collection):
        """Initialize the recorder."""
        self.uri = uri
        self.database_name = database
        self.collection_name = collection

    def write(self, results):
        """Insert results into the database."""
        client = MongoClient(self.uri)
        db = client[self.database_name]
        collection = db[self.collection_name]
        collection.insert_one(results)