# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/utils/patient.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 699 bytes
import logging
LOG = logging.getLogger(__name__)

def patients(database, ids=None):
    """Get all patients in the database

    Args:
        database(pymongo.database.Database)
        ids(list): a list of IDs to return only specified patients

    Returns:
        results(Iterable[dict]): list of patients from mongodb patients collection
    """
    results = None
    query = {}
    if ids:
        LOG.info('Querying patients for IDs {}'.format(ids))
        query['_id'] = {'$in': ids}
    else:
        LOG.info('Return all patients in database')
    results = database['patients'].find(query)
    return results