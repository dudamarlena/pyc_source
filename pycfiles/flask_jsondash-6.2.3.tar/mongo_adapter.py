# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/taborc/git/spog/flask_jsondash/flask_jsondash/mongo_adapter.py
# Compiled at: 2017-05-30 11:36:41
"""
flask_jsondash.mongo_adapter
~~~~~~~~~~~~~~~~~~~~~~~~~~

Adapters for various storage engines.

:copyright: (c) 2016 by Chris Tabor.
:license: MIT, see LICENSE for more details.
"""
from datetime import datetime as dt

class Db(object):
    """Adapter for all mongo operations."""

    def __init__(self, client, conn, coll, formatter):
        """Setup connection.

        Args:
            client (object): The database client to use.
            conn (str): The connection URI.
            coll (str): The collection name.
            formatter (function): A formatter function to use when formatting
                chart data.
        """
        self.client = client
        self.conn = conn
        self.coll = coll
        self.formatter = formatter

    def count(self, **kwargs):
        """Standard db count."""
        return self.coll.count(**kwargs)

    def read(self, **kwargs):
        """Read a record."""
        if kwargs.get('c_id') is None:
            return self.coll.find(**kwargs)
        else:
            return self.coll.find_one(dict(id=kwargs.pop('c_id')))
            return

    def update(self, c_id, data=None, fmt_charts=True):
        """Update a record.

        Args:
            c_id (int): The records id.
            data (None, optional): data to update the record with.
            fmt_charts (True, optional): A flag to fmt_charts with the
                default provided formatter.
        """
        if data is None:
            return
        else:
            charts = self.formatter(data) if fmt_charts else data.get('modules')
            save_conf = {'$set': {'layout': data.get('layout', 'freeform'), 
                        'name': data.get('name', 'NONAME'), 
                        'modules': charts, 
                        'date': dt.now()}}
            save_conf['$set'].update(**data)
            self.coll.update(dict(id=c_id), save_conf)
            return

    def create(self, data=None):
        """Add a new record.

        Args:
            data (dict): The "record" to insert.
        """
        if data is None:
            return
        else:
            self.coll.insert(data)
            return

    def delete(self, c_id):
        """Delete a record.

        Args:
            c_id (int): The records id.
        """
        self.coll.delete_one(dict(id=c_id))

    def delete_all(self):
        """Delete ALL records. Separated function for safety.

        This should never be used for production.
        """
        self.coll.remove()