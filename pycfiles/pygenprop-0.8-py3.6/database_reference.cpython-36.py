# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/database_reference.py
# Compiled at: 2019-04-04 13:26:37
# Size of source mod 2**32: 1002 bytes
"""
Created by: Lee Bergstrand (2017)

Description: The database reference class.
"""

class DatabaseReference(object):
    __doc__ = 'A class representing an external database reference for a genome property.'

    def __init__(self, database_name, record_title, record_ids):
        """
        Creates a new DatabaseReference object.

        :param database_name: The name of the database in question.
        :param record_title: The title of the record of the genome property in the database.
        :param record_ids: One or more database identifiers of the record of the genome property in the database.
        """
        self.database_name = database_name
        self.record_title = record_title
        self.record_ids = record_ids

    def __repr__(self):
        repr_data = [
         'Title: ' + str(self.record_title),
         'DB_Name: ' + str(self.database_name),
         'DB_Records: ' + str(self.record_ids)]
        return ', '.join(repr_data)