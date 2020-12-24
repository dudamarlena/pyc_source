# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mbe/logging.py
# Compiled at: 2015-09-01 20:16:32
# Size of source mod 2**32: 5855 bytes
"""
The logging module handles all the logging of MBE.
"""
import datetime
from mbe.misc.schema_mongodb import mbe_object_id
__author__ = 'nibo'

class DictDiffer(object):
    __doc__ = '\n    Calculate the difference between two dictionaries as:\n    (1) items added\n    (2) items removed\n    (3) keys same in both but changed values\n    (4) keys same in both and unchanged values\n\n    '

    def __init__(self, current_dict, past_dict):
        """
        Compares two dicts

        :param current_dict: The correct dict
        :param past_dict: The old dict

        """
        self.current_dict, self.past_dict = current_dict, past_dict
        self.current_keys, self.past_keys = [set(d.keys()) for d in (current_dict, past_dict)]
        self.intersect = self.current_keys.intersection(self.past_keys)

    def added(self):
        """
        A list of added items

        """
        return self.current_keys - self.intersect

    def removed(self):
        """
        Returns a list of removed items

        """
        return self.past_keys - self.intersect

    def changed(self):
        """
        Returns a list of changed items

        """
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    def unchanged(self):
        """
        Returns a list of unchanged items

        """
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


class Logging:
    __doc__ = '\n    The logging class provides functionality to properly write to the "log" collection\n    '
    database = None
    _log_collection = None

    def __init__(self, _database):
        """
        Initialize the logger, connects to a database

        :param _database:

        """
        self.database = _database
        self._log_collection = self.database['log']

    @staticmethod
    def _compare_documents(_left, _right):
        _changes = []
        _differ = DictDiffer(_left, _right)
        for _property in _differ.added():
            _changes.append({'propertyId': _property,  'before': None,  'after': _right[_property]})

        for _property in _differ.removed():
            _changes.append({'propertyId': _property,  'before': _left[_property],  'after': None})

        for _property in _differ.changed():
            _changes.append({'propertyId': _property,  'before': _left[_property],  'after': _right[_property]})

        return _changes

    @staticmethod
    def _generate_event_skeleton(_user_id, _occurred_when, _node_id):
        """
        Generate a skeleton for a event item

        :param _user_id: The userId
        :param _occurred_when: When the event occured
        :param _node_id: The affected nodeId

        """
        return {'user_id': mbe_object_id(_user_id), 
         'occurredWhen': _occurred_when, 
         'node_id': mbe_object_id(_node_id), 
         'event': {}}

    def write_log(self, _event):
        """
        Writes an event to the database

        :param _event: The event data

        """
        _event['writtenWhen'] = str(datetime.datetime.utcnow())
        self._log_collection.save(_event)

    def log_security(self, _type, _message, _user_id, _node_id):
        """
        Creates an security event log item

        :param _type: type of event, can be rights, access or attack
        :param _message: Error message
        :param _user_id: The _id of the user. A string(not the ObjectId)
        :param _node_id: If applicable, the concerned node document
        :return:

        """
        _event = self._generate_event_skeleton(_user_id, str(datetime.datetime.utcnow()), _node_id)
        _event['event'] = {'security': {'type': _type,  'message': _message}}
        self.write_log(_event)

    def log_save(self, _document, _user_id, _old_document=None):
        """
        Creates an event item based on the differences between the provided documents

        :param _document: The new version of the document
        :param _user_id: The _id of the user. A string(not the ObjectId)
        :param _old_document: The previous version

        """
        _event = self._generate_event_skeleton(_user_id, str(datetime.datetime.utcnow()), _document['_id'])
        if _old_document:
            _event['event']['change'] = self._compare_documents(_old_document, _document)
        else:
            _event['event']['add'] = _document
        self.write_log(_event)

    def log_remove(self, _removed_document, _user_id):
        """
        Created a "remove" event. Called when a document has been removed.

        :param _removed_document: The removed document.
        :param _user_id: The _id of the user. A string(not the ObjectId)

        """
        _event = self._generate_event_skeleton(_user_id, str(datetime.datetime.utcnow()), _removed_document['_id'])
        _event['event']['remove'] = _removed_document
        self.write_log(_event)