# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/snuba/json_schemas.py
# Compiled at: 2019-09-04 11:05:35
from __future__ import absolute_import
SUBSCRIPTION_WRAPPER_SCHEMA = {'type': 'object', 
   'properties': {'version': {'type': 'integer'}, 'payload': {'type': 'object'}}, 'required': [
              'version', 'payload'], 
   'additionalProperties': False}
SUBSCRIPTION_PAYLOAD_VERSIONS = {1: {'type': 'object', 
       'properties': {'subscription_id': {'type': 'string', 'minLength': 1}, 'values': {'type': 'object', 
                                 'minProperties': 1, 
                                 'additionalProperties': {'type': 'number'}}, 
                      'timestamp': {'type': 'number', 'minimum': 0}, 'interval': {'type': 'number', 'minimum': 0}, 'partition': {'type': 'number'}, 'offset': {'type': 'number'}}, 
       'required': [
                  'subscription_id', 'values', 'timestamp', 'interval', 'partition', 'offset'], 
       'additionalProperties': False}}