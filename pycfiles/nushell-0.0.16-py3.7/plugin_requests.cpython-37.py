# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nushell/tests/plugin_requests.py
# Compiled at: 2019-10-27 12:41:56
# Size of source mod 2**32: 3677 bytes
config_request = {'jsonrpc':'2.0', 
 'method':'config',  'params':[]}
sink_named_request = {'jsonrpc':'2.0', 
 'method':'sink', 
 'params':[
  {'args':{'positional':None, 
    'named':{'sink': {'tag':{'anchor':None, 
               'span':{'start':10, 
                'end':14}}, 
              'item':{'Primitive': {'Boolean': True}}}}}, 
   'name_tag':{'anchor':None, 
    'span':{'start':0, 
     'end':7}}}, []]}
sink_help_request = {'jsonrpc':'2.0', 
 'method':'sink', 
 'params':[
  {'args':{'positional':None, 
    'named':{'help': {'tag':{'anchor':None, 
               'span':{'start':10, 
                'end':14}}, 
              'item':{'Primitive': {'Boolean': True}}}}}, 
   'name_tag':{'anchor':None, 
    'span':{'start':0, 
     'end':7}}}, []]}
filter_begin_request = {'jsonrpc':'2.0', 
 'method':'begin_filter', 
 'params':{'args':{'positional':None, 
   'named':{'help': {'tag':{'anchor':None, 
              'span':{'start':6, 
               'end':10}}, 
             'item':{'Primitive': {'Boolean': True}}}}}, 
  'name_tag':{'anchor':None, 
   'span':{'start':0, 
    'end':3}}}}
filter_end_request = {'jsonrpc':'2.0', 
 'method':'end_filter',  'params':[]}
filter_string_request = {'jsonrpc':'2.0', 
 'method':'filter', 
 'params':{'tag':{'anchor':None, 
   'span':{'start':0, 
    'end':2}}, 
  'item':{'Primitive': {'String': 'pancakes'}}}}
filter_int_request = {'jsonrpc':'2.0', 
 'method':'filter', 
 'params':{'tag':{'anchor':None, 
   'span':{'start':0, 
    'end':2}}, 
  'item':{'Primitive': {'Int': 'imanumber'}}}}
filter_custom_request = {'jsonrpc':'2.0', 
 'method':'filter', 
 'params':{'tag':{'anchor':None, 
   'span':{'start':0, 
    'end':2}}, 
  'item':{'Primitive': {'Any': 'imathing'}}}}