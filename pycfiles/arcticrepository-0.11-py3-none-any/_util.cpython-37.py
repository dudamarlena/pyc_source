# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/_util.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 2988 bytes
import logging, numpy as np, pymongo
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal
from ._config import FW_POINTERS_CONFIG_KEY, FwPointersCfg
logger = logging.getLogger(__name__)
NP_OBJECT_DTYPE = np.dtype('O')
_use_new_count_api = None

def get_fwptr_config(version):
    return FwPointersCfg[version.get(FW_POINTERS_CONFIG_KEY, FwPointersCfg.DISABLED.name)]


def _detect_new_count_api():
    try:
        mongo_v = [int(v) for v in pymongo.version.split('.')]
        return mongo_v[0] >= 3 and mongo_v[1] >= 7
    except:
        return False


def indent(s, num_spaces):
    s = s.split('\n')
    s = [num_spaces * ' ' + line for line in s]
    s = '\n'.join(s)
    return s


def are_equals(o1, o2, **kwargs):
    try:
        if isinstance(o1, DataFrame):
            assert_frame_equal(o1, o2, kwargs)
            return True
        return o1 == o2
    except Exception:
        return False


def enable_sharding(arctic, library_name, hashed=True, key='symbol'):
    """
    Enable sharding on a library

    Parameters:
    -----------
    arctic: `arctic.Arctic` Arctic class

    library_name: `basestring` library name

    hashed: `bool` if True, use hashed sharding, if False, use range sharding
            See https://docs.mongodb.com/manual/core/hashed-sharding/,
            as well as https://docs.mongodb.com/manual/core/ranged-sharding/ for details.

    key: `basestring` key to be used for sharding. Defaults to 'symbol', applicable to
         all of Arctic's built-in stores except for BSONStore, which typically uses '_id'.
         See https://docs.mongodb.com/manual/core/sharding-shard-key/ for details.
    """
    c = arctic._conn
    lib = arctic[library_name]._arctic_lib
    dbname = lib._db.name
    library_name = lib.get_top_level_collection().name
    try:
        c.admin.command('enablesharding', dbname)
    except pymongo.errors.OperationFailure as e:
        try:
            if 'already enabled' not in str(e):
                raise
        finally:
            e = None
            del e

    if not hashed:
        logger.info("Range sharding '" + key + "' on: " + dbname + '.' + library_name)
        c.admin.command('shardCollection', (dbname + '.' + library_name), key={key: 1})
    else:
        logger.info("Hash sharding '" + key + "' on: " + dbname + '.' + library_name)
        c.admin.command('shardCollection', (dbname + '.' + library_name), key={key: 'hashed'})


def mongo_count(collection, filter=None, **kwargs):
    global _use_new_count_api
    filter = {} if filter is None else filter
    _use_new_count_api = _detect_new_count_api() if _use_new_count_api is None else _use_new_count_api
    if _use_new_count_api:
        return (collection.count_documents)(filter=filter, **kwargs)
    return (collection.count)(filter=filter, **kwargs)