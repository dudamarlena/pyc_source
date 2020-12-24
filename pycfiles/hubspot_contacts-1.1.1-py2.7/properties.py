# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hubspot/contacts/_schemas/properties.py
# Compiled at: 2017-11-13 03:44:28
from voluptuous import Any
from voluptuous import Schema
from hubspot.contacts.properties import PROPERTY_TYPE_BY_NAME
PROPERTY_RESPONSE_SCHEMA_DEFINITION = {'name': unicode, 
   'type': Any(*PROPERTY_TYPE_BY_NAME.keys()), 
   'options': []}
CREATE_PROPERTY_RESPONSE_SCHEMA = Schema(PROPERTY_RESPONSE_SCHEMA_DEFINITION, required=True, extra=True)
_GET_ALL_PROPERTIES_RESPONSE_SCHEMA_DEFINITION = [
 PROPERTY_RESPONSE_SCHEMA_DEFINITION]
GET_ALL_PROPERTIES_RESPONSE_SCHEMA = Schema(_GET_ALL_PROPERTIES_RESPONSE_SCHEMA_DEFINITION, required=True, extra=True)