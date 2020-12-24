# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/flo/Phoenics/master/src/phoenics/DatabaseHandler/SqliteInterface/sqlite_interface.py
# Compiled at: 2019-11-24 14:26:11
# Size of source mod 2**32: 6217 bytes
"""
Licensed to the Apache Software Foundation (ASF) under one or more 
contributor license agreements. See the NOTICE file distributed with this 
work for additional information regarding copyright ownership. The ASF 
licenses this file to you under the Apache License, Version 2.0 (the 
"License"); you may not use this file except in compliance with the 
License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
License for the specific language governing permissions and limitations 
under the License.

The code in this file was developed at ChemOS Inc. (2019).
"""
__author__ = 'Florian Hase'
import uuid, time, copy, sqlalchemy as sql
from . import AddEntry, FetchEntries, UpdateEntries
from utilities import Logger
from utilities.decorators import thread

class SQLiteDatabase(Logger):
    SQLITE_COLUMNS = {'float':sql.Float(), 
     'bool':sql.Boolean(), 
     'integer':sql.Integer(), 
     'pickle':sql.PickleType(), 
     'string':sql.String(512)}

    def __init__(self, path, attributes, name='table', verbosity=0):
        self.WRITING_REQUESTS = []
        self.READING_REQUESTS = {}
        self.UPDATE_REQUESTS = []
        Logger.__init__(self, 'SQLite interface', verbosity=verbosity)
        self.db_path = 'sqlite:///%s' % path
        self.attributes = attributes
        self.name = name
        self.log('creating database %s at %s' % (self.name, self.db_path), 'DEBUG')
        self.db = sql.create_engine(self.db_path)
        self.db.echo = False
        self.metadata = sql.MetaData(self.db)
        self.table = sql.Table(self.name, self.metadata)
        for name, att_type in self.attributes.items():
            self.table.append_column(sql.Column(name, self.SQLITE_COLUMNS[att_type]))

        self.table.create(checkfirst=True)
        self._process_requests()

    def _return_dict(function):

        def wrapper(self, *args, **kwargs):
            entries = function(self, *args, **kwargs)
            info_dicts = [{key:entry[key] for key in self.attributes} for entry in entries]
            return info_dicts

        return wrapper

    @thread
    def _process_requests(self):
        self._processing_requests = True
        keep_processing = True
        iteration_index = 0
        while keep_processing:
            num_reading_requests = len(self.READING_REQUESTS)
            num_writing_requests = len(self.WRITING_REQUESTS)
            num_update_requests = len(self.UPDATE_REQUESTS)
            iteration_index += 1
            request_keys = copy.deepcopy(list(self.READING_REQUESTS.keys()))
            for request_key in request_keys:
                if not self.READING_REQUESTS[request_key].executed:
                    self.READING_REQUESTS[request_key].execute()
                    break

            for update_index in range(num_update_requests):
                update_request = self.UPDATE_REQUESTS.pop()
                update_request.execute()

            if num_writing_requests > 0:
                writing_request = self.WRITING_REQUESTS.pop()
                writing_request.execute()
            request_keys = copy.deepcopy(list(self.READING_REQUESTS.keys()))
            delete_keys = []
            for request_key in request_keys:
                if self.READING_REQUESTS[request_key].entries_fetched:
                    delete_keys.append(request_key)

            for request_key in delete_keys:
                del self.READING_REQUESTS[request_key]

            keep_processing = len(self.WRITING_REQUESTS) > 0 or len(self.UPDATE_REQUESTS) > 0 or len(self.READING_REQUESTS) > 0

        self._processing_requests = False

    def add(self, info_dict):
        add_entry = AddEntry(self.db, self.table, info_dict)
        self.WRITING_REQUESTS.append(add_entry)
        if not self._processing_requests:
            self._process_requests()

    @_return_dict
    def fetch_all(self, condition_dict):
        condition_keys = list(condition_dict.keys())
        condition_values = list(condition_dict.values())
        selection = sql.select([self.table])
        for index, key in enumerate(condition_keys):
            if isinstance(condition_values[index], list):
                if len(condition_values[index]) == 0:
                    return []
                filters = [getattr(self.table.c, key) == value for value in condition_values[index]]
                condition = (sql.or_)(*filters)
            else:
                condition = getattr(self.table.c, key) == condition_values[index]
            selection = selection.where(condition)

        fetch_entries = FetchEntries((self.db), (self.table), selection, name=(self.name))
        fetch_keys = str(uuid.uuid4())
        self.READING_REQUESTS[fetch_keys] = fetch_entries
        if not self._processing_requests:
            self._process_requests()
        entries = fetch_entries.get_entries()
        self.log('fetched all information from database %s' % self.name, 'DEBUG')
        return entries

    def update_all(self, condition_dict, update_dict):
        condition_keys = list(condition_dict.keys())
        condition_values = list(condition_dict.values())
        update = sql.update(self.table).values(update_dict).where(getattr(self.table.c, condition_keys[0]) == condition_values[0])
        for index, key in enumerate(condition_keys[1:]):
            update = update.where(getattr(self.table.c, key) == condition_values[(index + 1)])

        update_entries = UpdateEntries(self.db, self.table, update)
        self.WRITING_REQUESTS.append(update_entries)
        if not self._processing_requests:
            self._process_requests()