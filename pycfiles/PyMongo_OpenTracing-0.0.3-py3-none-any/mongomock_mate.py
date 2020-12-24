# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pymongo_mate-project/pymongo_mate/mongomock_mate.py
# Compiled at: 2017-10-12 14:36:33
from superjson import json
try:
    from .pkg.sixmini import iteritems
except:
    from pymongo_mate.pkg.sixmini import iteritems

def _dump(db):
    """
    Dump :class:`mongomock.database.Database` to dict data.
    """
    db_data = {'name': db.name, '_collections': dict()}
    for col_name, collection in iteritems(db._collections):
        if col_name != 'system.indexes':
            col_data = {'_documents': collection._documents, '_uniques': collection._uniques}
            db_data['_collections'][col_name] = col_data

    return db_data


def _load(db_data, db):
    """
    Load :class:`mongomock.database.Database` from dict data.
    """
    if db.name != db_data['name']:
        raise ValueError("dbname doesn't matches! Maybe wrong database data.")
    db.__init__(client=db._client, name=db.name)
    for col_name, col_data in iteritems(db_data['_collections']):
        collection = db.get_collection(col_name)
        collection._documents = col_data['_documents']
        collection._uniques = col_data['_uniques']
        db._collections[col_name] = collection

    return db


def dump_db(db, file, pretty=False, overwrite=False, verbose=True):
    """
    Dump :class:`mongomock.database.Database` to a local file. Only support
    ``*.json`` or ``*.gz`` (compressed json file)

    :param db: instance of :class:`mongomock.database.Database`.
    :param file: file path.
    :param pretty: bool, toggle on jsonize into pretty format.
    :param overwrite: bool, allow overwrite to existing file.
    :param verbose: bool, toggle on log.
    """
    db_data = _dump(db)
    json.dump(db_data, file, pretty=pretty, overwrite=overwrite, verbose=verbose)


def load_db(file, db, verbose=True):
    """
    Load :class:`mongomock.database.Database` from a local file.

    :param file: file path.
    :param db: instance of :class:`mongomock.database.Database`.
    :param verbose: bool, toggle on log.
    :return: loaded db.
    """
    db_data = json.load(file, verbose=verbose)
    return _load(db_data, db)