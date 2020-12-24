# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/recorders/sqldatabase.py
# Compiled at: 2017-04-12 08:01:58
# Size of source mod 2**32: 1950 bytes
"""Exposes the SQLDatabase result recorder."""
import json
try:
    from sqlalchemy import create_engine, text
except ImportError:
    pass

class SQLDatabase(object):
    __doc__ = 'Record results to a database supported by SQLAlchemy.\n\n    Args:\n        uri (str): database server URI e.g. ``mysql://username:password@localhost/dbname``\n        table (str): table name\n        values (dict): a mapping from database table columns to values\n\n    Keyword Args:\n        json_column (str): If supplied the complete result dictionary will be written to this column\n\n    See Also:\n        `SQLAlchemy documentation <http://docs.sqlalchemy.org/en/latest/core/connections.html>`_\n    '

    def __init__(self, uri, table, values, json_column=None):
        """Initialize the recorder."""
        self.uri = uri
        self.table = table
        self.values = values
        self.json_column = json_column

    def write(self, results):
        """Write the results to the database table specified at initialisation.

        Args:
            results (dict): A dictionary of results to record
        """
        engine = create_engine(self.uri)
        field_names = ','.join(self.values.keys())
        values_placeholder = ','.join([':{0}'.format(k) for k in self.values.keys()])
        if self.json_column is not None:
            field_names += ',' + self.json_column
            values_placeholder += ',:_JSON_'
        query_string = '\n            INSERT INTO {table}\n            ({field_names})\n            VALUES ({values_placeholder})\n        '
        query = text(query_string.format(table=(self.table),
          field_names=field_names,
          values_placeholder=values_placeholder))
        row = {}
        for field in self.values:
            row[field] = self.values[field](results)

        if self.json_column is not None:
            row['_JSON_'] = json.dumps(results)
        (engine.execute)(query, **row)