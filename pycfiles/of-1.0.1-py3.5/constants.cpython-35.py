# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/schemas/constants.py
# Compiled at: 2016-09-15 19:55:30
# Size of source mod 2**32: 2279 bytes
"""
The constants module holds constants for all the schemas defined in Optimal Framework

Created on Jan 22, 2016

@author: Nicklas Boerjesson
"""
__author__ = 'Nicklas Borjesson'
id_administration = '000000010000010001e64c23'
id_groups = '000000010000010001e64c24'
id_users = '000000010000010001e64c25'
id_rights = '000000010000010001e64c26'
id_right_admin_everything = '000000010000010001e64c27'
id_group_administrators = '000000010000010001e64c28'
id_group_users = '000000010000010001e64c29'
id_peers = '000000010000010002e64d03'
id_templates = '000000010000010002e64d04'
zero_object_id = '000000000000000000000000'
schema_categories = {'ref://of.message.message': 'message', 
 'ref://of.message.error': 'message', 
 'ref://of.node.broker': 'node', 
 'ref://of.node.admin': 'node', 
 'ref://of.node.peer': 'node', 
 'ref://of.log.progression': 'log', 
 'ref://of.log.process_state': 'log', 
 'ref://of.event': 'log', 
 'ref://of.process.system': 'process'}
intercept_schema_ids = []
peer_type__schema_id = {'broker': 'ref://of.node.broker', 
 'admin': 'ref://of.node.admin', 
 'peer': 'ref://of.node.peer'}

def peer_type_to_schema_id(_peer_type):
    if _peer_type in peer_type__schema_id:
        return peer_type__schema_id[_peer_type]
    raise Exception('Invalid peer type:' + _peer_type)