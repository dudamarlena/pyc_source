# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/api/tree/access.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on Sep 4, 2012

@author: Nicklas Boerjesson
"""
from qal.sql.sql_xml import SQL_XML
from ube.concerns.connection import connection_c
from ube.concerns.internal import not_implemented
from ube.concerns.memoize import memoized
from ube.api.tree.node import node
from ube.api.tree.const import dmNone, dmEAV, dmSubtable, dmUBPMXML, etNODE_CREATED, etNODE_DELETED, etNODE_MODIFIED
from os.path import dirname
from uuid import uuid1

@connection_c
class access(object):
    """
    The access class  handles all CRUD operations to the UBPM database 
    tree structure and its related tables,
    The tree has 3 different storage models, however it is possible that "Tree with EAV" will be the only one. 
    """
    _dal = None

    def __init__(self):
        """
        Constructor
        """
        self.Nodes_Script_Dir = dirname(__file__)
        self.Nodes_XML_Dir = self.Nodes_Script_Dir + '/resources/xml'

    @memoized
    def load_fields(self, _nodetypeid):
        """Load fields for a specified node type"""
        _new_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/load_fields_nodetypeid.xml', nodetypeid=_nodetypeid)
        _tmpSQL = _new_sql_struct.as_sql(self._dal.db_type)
        try:
            _fields = self._dal.query(_tmpSQL)
        except Exception as e:
            raise Exception('access.create_new: Exception loading fields. Error:\n' + str(e) + '\nSQL:\n' + _tmpSQL)

        _result = []
        for _curr_field in _fields:
            _result.append(_curr_field)

        return _result

    def init_nodefields(self, _node, _nodetypeid):
        """Initialise a node object with the fields associated with a certain node type"""
        _fields = self.load_fields(_nodetypeid)
        for _curr_field in _fields:
            if _curr_field[4].lower() == 'string':
                _node.__setattr__(_curr_field[2], str(_curr_field[3]))
            elif _curr_field[4].lower() == 'numeric':
                _node.__setattr__(_curr_field[2], float(_curr_field[3]))
            else:
                raise Exception('access.create_new: Internal error setting defaults. Invalid datatype in Node_Field.Datatype: ' + _curr_field[4])

    def group_nodes(self, _nodes, _fieldname):
        """Group nodes by the specified field name"""
        sortkeyfn = lambda x: x.__getattribute__(_fieldname)
        _nodes = sorted(_nodes, key=sortkeyfn)
        from itertools import groupby
        _result = []
        for key, valuesiter in groupby(_nodes, key=sortkeyfn):
            _result.append((key, list(v for v in valuesiter)))

        return _result

    def create_new(self, _parentnodeid, _nodetypeid, _nodename):
        """Creates a new node object and populates it with it's defaults."""
        _nodeuuid = uuid1()
        _new_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/create_new_node.xml', parentnodeid=_parentnodeid, nodetypeid=_nodetypeid, nodeuuid=_nodeuuid, nodename=_nodename)
        _event_log_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/create_event_matrix.xml')
        _event_log_sql_struct.data.data_source.field_names = ['EventLogUUId', 'UserNodeId', 'SessionId', 'EventTypeId']
        _node_history_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/write_node_history_matrix.xml')
        _node_history_sql_struct.data.data_source.field_names = ['EventLogUUId', 'FieldUUId', 'NewValue']
        try:
            tmpSQL = _new_sql_struct.as_sql(self._dal.db_type)
            try:
                self._dal.execute(tmpSQL)
                self._dal.commit()
            except Exception as e:
                raise Exception('access.create_new: Exception creating node. Error:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            _new_node = self.load_nodes(_nodeuuids=[str(_nodeuuid)])[0]
            _hard_coded_usernodeid = 0
            _hard_coded_sessionid = 1234
            _hard_coded_event_typeid = etNODE_CREATED
            _EventLogUUId = str(uuid1())
            _event_log_sql_struct.data.data_source.data_table.append([_EventLogUUId, _hard_coded_usernodeid, _hard_coded_sessionid, _hard_coded_event_typeid])
            _node_history_sql_struct.data.data_source.data_table.append([_EventLogUUId, _new_node.nodeid, '', 'Node created'])
            tmpSQL = _event_log_sql_struct.as_sql(self._dal.db_type)
            try:
                self._dal.execute(tmpSQL)
                self._dal.commit()
            except Exception as e:
                raise Exception('access.create_new: Exception writing to event log node. Error:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            tmpSQL = _node_history_sql_struct.as_sql(self._dal.db_type)
            try:
                self._dal.execute(tmpSQL)
                self._dal.commit()
            except Exception as e:
                raise Exception('access.create_new: Exception writing to node history. Error:\n' + str(e) + '\nSQL:\n' + tmpSQL)

        except Exception as e:
            self._dal.rollback()
            raise Exception(str(e) + '\nOperation rolled back')

        try:
            self._dal.commit()
        except Exception as e:
            raise Exception('access.create_new: Error committing transaction:\n' + str(e) + '\nSQL:\n' + tmpSQL)

        self.init_nodefields(_new_node, _new_node.nodetypeid)
        return _new_node

    @not_implemented
    def list_permissions(self, _nodeids):
        """Returns the users permissions on each of the selected nodes"""
        _result = []
        return _result

    @not_implemented
    def _check_permissions(self, _nodeids, _asked_permission):
        """Check whether a user has a certain permission"""
        _violations = []
        return _violations

    def load_nodes(self, _nodeids=None, _nodeuuids=None, _parentnodeids=None, _with_data=None, _with_EAV_metadata=None):
        """Constructs database queries given a list of nodeids that retrieves 
        the relevant data from the database by populating node objects."""
        result = []
        if _nodeids != None:
            _nodeidstring = ', '.join(str(x) for x in _nodeids)
            _new_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/load_nodes_nodeids.xml', nodeids=_nodeidstring)
        else:
            if _nodeuuids != None:
                _nodeuuidstring = "'" + "', '".join(_nodeuuids) + "'"
                _new_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/load_nodes_nodeuuids.xml', nodeuuids=_nodeuuidstring)
            elif _parentnodeids != None:
                _parentnodeidstring = ', '.join(_parentnodeids)
                _new_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/load_nodes_parentnodeids.xml', nodeuuids=_parentnodeidstring)
        tmpSQL = _new_sql_struct.as_sql(self._dal.db_type)
        try:
            dsnodes = self._dal.query(tmpSQL)
        except Exception as e:
            raise Exception('DBUpgrader.add_to_application: Exception executing statement:\n' + str(e) + '\nSQL:\n' + tmpSQL)

        for curr_row in dsnodes:
            new_node = node(_nodeid=curr_row[0], _parentnodeid=curr_row[1], _nodetypeid=curr_row[2], _nodeuuid=curr_row[3], _nodename=curr_row[4], _datamodelid=curr_row[5])
            result.append(new_node)

        if result and _with_data:
            self.load_datas(result)
        return result

    def load_datas(self, _nodes):
        """Load the data associated to a list of nodes"""
        _groups = self.group_nodes(_nodes, 'nodetypeid')
        for _curr_nodetypeid, _curr_nodes in _groups:
            if _curr_nodes[0].datamodelid == dmNone:
                pass
            elif _curr_nodes[0].datamodelid == dmSubtable:
                self.load_datas_Subtable(_curr_nodes, _curr_nodetypeid)
            elif _curr_nodes[0].datamodelid == dmEAV:
                self.load_datas_EAV(_curr_nodes, _curr_nodetypeid)
            elif _curr_nodes[0].datamodelid == dmUBPMXML:
                self.load_datas_XML(_curr_nodes, _curr_nodetypeid)
            else:
                raise Exception('access.load_datas: Invalid datamodelid : ' + str(_curr_nodes[0].datamodelid))

    def load_datas_EAV(self, _nodes, _nodetypeid):
        """Load the data associated to a list of nodes that are known to only use the EAV data model"""
        sorted(_nodes, key=lambda _curr_node: _curr_node.nodeid)
        _nodeidstring = ', '.join(str(_currnode.nodeid) for _currnode in _nodes)
        _load_datas_EAV_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/load_datas_EAV.xml', nodeids=_nodeidstring)
        try:
            _tmpSQL = _load_datas_EAV_struct.as_sql(self._dal.db_type)
            _datas = self._dal.query(_tmpSQL)
        except Exception as e:
            raise Exception('access.load_datas_EAV: Error loading node_EAV records:\n' + str(e) + '\nSQL:\n' + _tmpSQL)

        _curr_node = _nodes[0]
        self.init_nodefields(_curr_node, _nodetypeid)
        _currnode_idx = -1
        for _curr_data in _datas:
            if _curr_node.nodeid != _curr_data[0]:
                _currnode_idx = _currnode_idx + 1
                _curr_node = _nodes[_currnode_idx]
            _curr_node.__setattr__(_curr_data[3], _curr_data[2])

    def delete_nodes(self, _nodes):
        """Delete specified nodes and associated data from database"""
        _delete_EAV_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/clean_Node_EAV_matrix.xml')
        _delete_EAV_sql_struct.sources[1].expression[0].data_source.field_names = ['NodeId']
        _delete_node_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/delete_Node_matrix.xml')
        _delete_node_sql_struct.sources[1].expression[0].data_source.field_names = ['NodeId']
        _event_log_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/create_event_matrix.xml')
        _event_log_sql_struct.data.data_source.field_names = ['EventLogUUId', 'UserNodeId', 'SessionId', 'EventTypeId']
        _node_history_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/write_node_history_matrix.xml')
        _node_history_sql_struct.data.data_source.field_names = ['EventLogUUId', 'FieldUUId', 'NewValue']
        _hard_coded_usernodeid = 0
        _hard_coded_sessionid = 1234
        _hard_coded_event_typeid = etNODE_DELETED
        for _curr_node in _nodes:
            _EventLogUUId = str(uuid1())
            _delete_EAV_sql_struct.sources[1].expression[0].data_source.data_table.append([_curr_node.nodeid])
            _delete_node_sql_struct.sources[1].expression[0].data_source.data_table.append([_curr_node.nodeid])
            _event_log_sql_struct.data.data_source.data_table.append([_EventLogUUId, _hard_coded_usernodeid, _hard_coded_sessionid, _hard_coded_event_typeid])
            _node_history_sql_struct.data.data_source.data_table.append([_EventLogUUId, _curr_node.nodeid, '', 'Node deleted'])

        self._dal.autocommit = False
        try:
            try:
                tmpSQL = _delete_EAV_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.delete_nodes: Error deleting Node_EAV records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            try:
                tmpSQL = _delete_node_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.delete_nodes: Error deleting Node records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            try:
                tmpSQL = _event_log_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.delete_nodes: Error inserting event log records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            try:
                tmpSQL = _node_history_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.delete_nodes: Error inserting Node_History records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

        except Exception as e:
            self._dal.rollback()
            raise Exception(str(e) + '\nOperation rolled back')

        try:
            self._dal.commit()
        except Exception as e:
            raise Exception('access.delete_nodes: Error committing transaction:\n' + str(e) + '\nSQL:\n' + tmpSQL)

    @not_implemented
    def load_datas_subtable(self, _nodes, _nodetypeid):
        """Load the data associated to a list of nodes that are known to only use the subtable data model"""
        pass

    def write_EAV_changes(self, _changes):
        """Write all changes to the EAV data model and corresponding events to the event log"""
        _event_log_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/create_event_matrix.xml')
        _event_log_sql_struct.data.data_source.field_names = ['EventLogUUId', 'UserNodeId', 'SessionId', 'EventTypeId']
        _node_history_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/write_node_history_matrix.xml')
        _node_history_sql_struct.data.data_source.field_names = ['EventLogUUId', 'FieldUUId', 'NewValue']
        _delete_EAV_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/delete_Node_EAV_matrix.xml')
        _delete_EAV_sql_struct.sources[1].expression[0].data_source.field_names = ['NodeId', 'FieldUUId']
        _write_EAV_sql_struct = SQL_XML().xml_file_to_sql(self.Nodes_XML_Dir + '/write_Node_EAV_matrix.xml')
        _write_EAV_sql_struct.data.data_source.field_names = ['NodeId', 'FieldUUId', 'Value']
        _hard_coded_usernodeid = 0
        _hard_coded_sessionid = 1234
        _hard_coded_event_typeid = etNODE_MODIFIED
        _curr_nodeid = None
        sorted(_changes, key=lambda _curr_node: _curr_node[0])
        for _curr_change in _changes:
            if _curr_change[0] != _curr_nodeid:
                _EventLogUUId = str(uuid1())
                _event_log_sql_struct.data.data_source.data_table.append([_EventLogUUId, _hard_coded_usernodeid, _hard_coded_sessionid, _hard_coded_event_typeid])
                _curr_nodeid = _curr_change[0]
            _node_history_sql_struct.data.data_source.data_table.append([_EventLogUUId, _curr_change[0], _curr_change[1], _curr_change[2]])
            _delete_EAV_sql_struct.sources[1].expression[0].data_source.data_table.append([_curr_change[0], _curr_change[1]])
            _write_EAV_sql_struct.data.data_source.data_table.append([_curr_change[0], _curr_change[1], _curr_change[2]])

        self._dal.autocommit = False
        try:
            try:
                tmpSQL = _delete_EAV_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.write_EAV_changes: Error deleting old Node_EAV records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            try:
                tmpSQL = _write_EAV_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.write_EAV_changes: Error inserting old Node_EAV records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            try:
                tmpSQL = _event_log_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.write_EAV_changes: Error inserting event log records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

            try:
                tmpSQL = _node_history_sql_struct.as_sql(self._dal.db_type)
                self._dal.execute(tmpSQL)
            except Exception as e:
                raise Exception('access.write_EAV_changes: Error inserting Node_History records:\n' + str(e) + '\nSQL:\n' + tmpSQL)

        except Exception as e:
            self._dal.rollback()
            raise Exception(str(e) + '\nOperation rolled back')

        try:
            self._dal.commit()
        except Exception as e:
            raise Exception('access.create_node_history: Error committing transaction:\n' + str(e) + '\nSQL:\n' + tmpSQL)

        return

    def save_nodes(self, _nodes):
        """Save specified nodes to the database"""
        _nodes_by_type = self.group_nodes(_nodes, 'nodetypeid')
        _changes = []
        for _curr_nodetypeid, _curr_nodes in _nodes_by_type:
            sorted(_curr_nodes, key=lambda _curr_node: _curr_node.nodeid)
            _orig_nodes = self.load_nodes(_nodeids=[_curr_orig_node.nodeid for _curr_orig_node in _curr_nodes])
            sorted(_orig_nodes, key=lambda _curr_node: _curr_node.nodeid)
            _fields = self.load_fields(_curr_nodetypeid)
            for _curr_idx in range(len(_curr_nodes)):
                _curr_new = _curr_nodes[_curr_idx]
                _curr_old = _orig_nodes[_curr_idx]
                for _curr_field in _fields:
                    if hasattr(_curr_new, _curr_field[2]):
                        _new_value = _curr_new.__getattribute__(_curr_field[2])
                        if hasattr(_curr_old, _curr_field[2]):
                            if _new_value != _curr_old.__getattribute__(_curr_field[2]):
                                _changes.append([_curr_new.nodeid, _curr_field[0], _new_value])
                        else:
                            _changes.append([_curr_new.nodeid, _curr_field[0], _new_value])
                            continue

        self.write_EAV_changes(_changes)