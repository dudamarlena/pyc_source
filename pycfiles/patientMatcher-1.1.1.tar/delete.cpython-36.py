# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/utils/delete.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 874 bytes
import logging
from pymongo import MongoClient
LOG = logging.getLogger(__name__)

def delete_by_query(query, mongo_db, mongo_collection):
    """Deletes one or more entries matching a query from a database collection

    Args:
        query(dict): query to be used for deleting the entries
        mongo_db(pymongo.database.Database)
        mongo_collection(str): the name of a collection

    Returns:
        deleted_entries(int): the number of deleted deleted entries or the error
    """
    LOG.info('Removing entries from collection "{0}" using the following parameters:{1}'.format(mongo_collection, query))
    deleted_entries = 0
    try:
        result = mongo_db[mongo_collection].delete_many(query)
        deleted_entries = result.deleted_count
    except Exception as err:
        deleted_entries = err

    return deleted_entries