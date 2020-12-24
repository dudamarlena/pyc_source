# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_jsondash/flask_jsondash/db.py
# Compiled at: 2017-05-30 11:38:02
# Size of source mod 2**32: 1606 bytes
"""
flask_jsondash.db
~~~~~~~~~~~~~~~~~~~~~~~~~~

A translation adapter for transparent operations between storage types.

:copyright: (c) 2016 by Chris Tabor.
:license: MIT, see LICENSE for more details.
"""
import json
from datetime import datetime as dt
from pymongo import MongoClient
from . import mongo_adapter, settings
DB_NAME = settings.ACTIVE_DB

def reformat_data(data, c_id):
    """Format/clean existing config data to be re-inserted into database.

    Args:
        data (dict): The chart data to override with standard params.

    Returns:
        data (dict): The in-place updated dict.
    """
    data.update(dict(id=c_id, date=dt.now()))
    return data


def format_charts(data):
    """Form chart POST data for JSON usage within db.

    Args:
        data (dict): The request.form data to format.

    Returns:
        modules (list): A list of json-decoded dictionaries.
    """
    modules = []
    for item in data:
        if item.startswith('module_'):
            val_json = json.loads(data[item])
            modules.append(val_json)

    return modules


def get_db_handler():
    """Get the appropriate db adapter.

    Returns:
        object: The instantiated database handler
    """
    if DB_NAME == 'mongo':
        client = MongoClient(host=settings.DB_URI, port=settings.DB_PORT)
        conn = client[settings.DB_NAME]
        coll = conn[settings.DB_TABLE]
        return mongo_adapter.Db(client, conn, coll, format_charts)
    raise NotImplementedError('Mongodb is the only supported database right now.')