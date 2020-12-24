# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/broker/lib/node.py
# Compiled at: 2016-09-16 05:33:36
# Size of source mod 2**32: 10718 bytes
"""
The node module provides the node-API for OF. All interaction with the node-collection should happen
through the Node-class

Note: Sphinx does not properly document this module with the decorators, comment them before running sphinx

Created on Mar 18, 2016

@author: Nicklas Boerjesson
"""
from bson.objectid import ObjectId
from of.broker.lib.auth_backend import MongoDBAuthBackend
from of.common.security.authentication import init_authentication
from of.common.security.groups import aop_has_right, init_groups
from of.broker.lib.schema_mongodb import of_object_id
from of.common.security.permission import filter_by_group
from of.forms import load_forms_from_directory, of_form_folder, cache as form_cache
from of.schemas.constants import id_right_admin_everything, id_templates
__author__ = 'nibo'
node_rights = None

def sanitize_node(_node):
    """
    Sanitize a node instance so that sensitive data isn't disseminated
    :param _node: The node to sanitize
    :return:
    """
    if 'credentials' in _node:
        _node.pop('credentials')
    if 'canRead' in _node:
        _node.pop('canRead')
    if 'canWrite' in _node:
        _node.pop('canWrite')
    return _node


def get_node_rights():
    """
    This function is necessary to hand runtime data to the decorators

    :return: the node rights

    """
    global node_rights
    return node_rights


class Node:
    __doc__ = '\n    The node class is used for all node management in OF.\n    '
    database_access = None
    rights = None

    def __init__(self, _database_access, _rights=None):
        """
        Initializes that node object and groups.

        :param _database_access: A database access instance

        """
        global node_rights
        if _database_access is None:
            raise Exception('Node: The database access parameter is None, it must be set for the Node class to work')
        self.database_access = _database_access
        if _rights is not None:
            node_rights = [
             id_right_admin_everything] + _rights
        else:
            node_rights = [
             id_right_admin_everything]
        init_groups(self.database_access)
        load_forms_from_directory(of_form_folder())

    def _string_to_object_ids(self, _data):
        if isinstance(_data, list):
            _destination = []
            for _curr_row in _data:
                _destination.append(self._string_to_object_ids(_curr_row))

            return _destination
        else:
            if isinstance(_data, dict):
                _destination = {}
                for _curr_key, _curr_value in _data.items():
                    _destination[_curr_key] = self._string_to_object_ids(_curr_value)

                return _destination
            if _data is not None and type(_data) != ObjectId and _data[:9] == 'ObjectId(':
                return ObjectId(_data[9:-1])
            return _data

    @aop_has_right(get_node_rights)
    def save(self, _document, _user):
        """save(self, _document, _user)

        Saves an of-node descendant to the database.

        :param _document: The node document to save.
        :param _user: The current user
        :return: A structure detailing the save result

        """
        self.database_access.verify_document(_document, 'node', 'Node.save')
        if '_id' in _document:
            _old_document_result = filter_by_group(self.database_access.find({'conditions': {'_id': of_object_id(_document['_id'])}, 'collection': 'node'}), 'canWrite', _user, 'Node.save(existing node)')
            if len(_old_document_result) == 1:
                _old_document = _old_document_result[0]
            else:
                raise Exception('Needed exactly one(1) existing node, found ' + str(len(_old_document_result)) + '. _id: ' + _document['_id'])
        else:
            if 'parent_id' in _document:
                filter_by_group(self.database_access.find({'conditions': {'_id': of_object_id(_document['parent_id'])}, 'collection': 'node'}), 'canWrite', _user, 'Node.save(new node)')
                _old_document = None
            else:
                raise Exception('Node.save: Data must have a parentId or an _id.')
        return self.database_access.save(_document, _user, _old_document)

    @aop_has_right(get_node_rights)
    def find(self, _conditions, _user, _error_prefix_if_not_allowed=None):
        """find(_conditions,_user)
        Returns a list of nodes matching the condition.
        Note: This method is literate, it takes ObjectId instances when comparing to ObjectId instances.
        But JSON doesn't handle ObjectId. So instead it supports an ObjectId(000000010000010001ee3214)-syntax
        and when it encounters those values, it converts them into ObjectId instances.

        :param _conditions: A condition
        :param _user: A user object
        :return: A list of nodes

        """
        return filter_by_group(self.database_access.find({'conditions': self._string_to_object_ids(_conditions), 'collection': 'node'}), 'canRead', _user, self.database_access, _error_prefix_if_not_allowed=_error_prefix_if_not_allowed)

    @aop_has_right(get_node_rights)
    def load_children(self, _parent_id, _user):
        """
        Returns a list of child nodes whose _parent_ids match _parent_id

        :param _parent_id: A parent Id
        :param _user: A user object
        :return: A list of nodes

        """
        return filter_by_group(self.database_access.find({'conditions': {'parent_id': of_object_id(_parent_id)}, 'collection': 'node'}), 'canRead', _user, self.database_access)

    @aop_has_right(get_node_rights)
    def load_node(self, _id, _user):
        """
        Returns the child with _id.

        :param _id: An object with a id property
        :param _user: A user object
        :return: A list of nodes

        """
        return filter_by_group(self.database_access.find({'conditions': {'_id': of_object_id(_id['_id'])}, 'collection': 'node'}), 'canRead', _user, self.database_access, _error_prefix_if_not_allowed='Node.load_node: Not permissioned to load this node. _id: ' + _id['_id'])[0]

    @aop_has_right(get_node_rights)
    def get_templates(self, _schema_ref, _user):
        """
        Returns a template.

        :param _schema_ref: The schemaRef if the wanted templates
        :return: A list of nodes matching the schema that the user have rights to

        """
        return filter_by_group(self.database_access.find({'conditions': {'parent_id': of_object_id(id_templates), 'schemaRef': _schema_ref}, 'collection': 'node'}), 'canRead', _user, self.database_access)

    @aop_has_right(get_node_rights)
    def lookup(self, _conditions, _user):
        """
        Returns a list of value-name objects for use in drop downs.
        As find, handles the ObjectId(000000010000010001ee3214) string format. (no quotes)

        :param _conditions: An MBE condition
        :param _user: A user object
        :return: A list of lookup objects.

        """
        self.database_access.verify_condition(_conditions, 'node', 'Node.find')
        print(str(_conditions))
        return [{'value': _row['_id'], 'text': _row['name']} for _row in filter_by_group(self.database_access.find(self._string_to_object_ids(_conditions)), 'canRead', _user, self.database_access)]

    @aop_has_right(get_node_rights)
    def remove(self, _id, _user):
        """
        Remove the specified node

        :param _id: An object with a node _id field
        :param _user: A user object
        :return: Result of removal

        """

        def _recurse_children(_parent_node):
            _result = [
             _parent_node]
            _child_nodes = self.database_access.find({'conditions': {'parent_id': _parent_node['_id']}, 'collection': 'node'}, _do_not_fix_object_ids=True)
            for _curr_child in _child_nodes:
                _result += _recurse_children(_curr_child)

            return _result

        _node = self.database_access.find({'conditions': {'_id': of_object_id(_id['_id'])}, 'collection': 'node'}, _do_not_fix_object_ids=True)[0]
        _all_nodes = _recurse_children(_node)
        _documents = filter_by_group(_all_nodes, 'canWrite', _user, self.database_access, _error_prefix_if_not_allowed='Node.remove: Missing permissions to remove node or sub nodes.', _use_object_id=True)
        return self.database_access.remove_documents(_documents, _user, 'node')

    @aop_has_right(get_node_rights)
    def history(self, _id, _user):
        """

        Return the change history for the specified node.

        :param _id: An object with a node _id field
        :param _user: A user object
        :return:

        """
        object_id = of_object_id(_id['_id'])
        filter_by_group(self.database_access.find({'conditions': {'_id': object_id}, 'collection': 'node'}), 'canRead', _user, self.database_access, _error_prefix_if_not_allowed='Node.history: No permissions to view details of this node. _id: ' + _id['_id'])
        return self.database_access.find({'conditions': {'node_id': object_id}, 'collection': 'log'})

    def get_schemas(self, _user):
        print('Request the schema database')
        return self.database_access.schema_tools.json_schema_objects

    def get_jsf_forms(self, _user):
        print('Request the JSF form database')
        return form_cache