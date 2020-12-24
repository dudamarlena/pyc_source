# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/go_http/tests/fixtures/account.py
# Compiled at: 2017-02-17 10:13:07
"""Fixtures for the account API."""
import copy
campaigns = [
 {'name': 'Your Campaign', 
    'key': 'key-hash-1'}]
channels = [
 {'endpoints': [
                {'uuid': 'TRANSPORT_TAG:tagpool:tagname::default', 
                   'name': 'default'}], 
    'tag': [
          'tagpool', 'tagname'], 
    'description': 'Tagpool: Tagname', 
    'name': 'A nice name', 
    'uuid': 'channel-uuid-1'}]
conversations = [
 {'type': 'dialogue', 
    'status': 'running', 
    'uuid': 'conv-1', 
    'name': 'Test Dialogue', 
    'endpoints': [
                {'uuid': 'CONVERSATION:dialogue:conv-1::default', 
                   'name': 'default'}], 
    'description': 'Small dialogue for testing'}]
routers = [
 {'status': 'running', 
    'description': 'Keyword router for my app', 
    'conversation_endpoints': [
                             {'uuid': 'ROUTER:keyword:rtr-1:OUTBOUND::default', 
                                'name': 'default'},
                             {'uuid': 'ROUTER:keyword:rtr-1:OUTBOUND::keyword_two', 
                                'name': 'keyword_two'},
                             {'uuid': 'ROUTER:keyword:rtr-1:OUTBOUND::keyword_one', 
                                'name': 'keyword_one'}], 
    'uuid': 'rtr-1', 
    'channel_endpoints': [
                        {'uuid': 'ROUTER:keyword:rtr-1:INBOUND::default', 
                           'name': 'default'}], 
    'type': 'keyword', 
    'name': 'Keywords for my app'}]
routing_entries = [
 {'source': {'uuid': 'TRANSPORT_TAG:tagpool:tagname::default'}, 
    'target': {'uuid': 'CONVERSATION:conv_type:conv-id-1::default'}}]
routing_table = copy.deepcopy({'channels': channels, 
   'conversations': conversations, 
   'routers': routers, 
   'routing_entries': routing_entries})