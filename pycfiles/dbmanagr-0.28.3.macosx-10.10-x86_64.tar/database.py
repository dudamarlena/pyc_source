# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/model/database.py
# Compiled at: 2015-10-11 07:17:06
from .baseitem import BaseItem
OPTION_URI_DATABASE_FORMAT = '{}/'
AUTOCOMPLETE_FORMAT = '{connection.user}@{connection.host}/{database}'

class Database(BaseItem):
    """The database used with the given connection"""

    def __init__(self, connection, name, autocomplete_format=AUTOCOMPLETE_FORMAT):
        self._connection = connection
        self.name = name
        self._autocomplete_format = autocomplete_format
        self.uri = repr(self)

    def __repr__(self):
        return self._autocomplete_format.format(connection=self._connection, database=self.name)

    def autocomplete(self):
        """Retrieves the autocomplete string"""
        return OPTION_URI_DATABASE_FORMAT.format(self.uri)