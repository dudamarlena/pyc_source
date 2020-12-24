# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hubspot/contacts/_schemas/contacts.py
# Compiled at: 2017-11-13 03:36:59
from voluptuous import All
from voluptuous import Any
from voluptuous import Length
from voluptuous import Schema
from hubspot.contacts._schemas._validators import AnyListItemValidates
from hubspot.contacts._schemas._validators import Constant
from hubspot.contacts._schemas._validators import DynamicDictionary
from hubspot.contacts._schemas._validators import GetDictValue
_CANONICAL_IDENTITY_PROFILE_SCHEMA = All([], AnyListItemValidates(Schema({'type': Constant('EMAIL'), 'value': unicode}, required=True, extra=True)))
_IS_PROPERTY_VALUE = Schema({'value': unicode}, required=True, extra=True)
_IDENTITY_PROFILE_SCHEMA = Schema({'vid': int, 'identities': Any([], _CANONICAL_IDENTITY_PROFILE_SCHEMA)}, extra=True, required=True)
CONTACT_SCHEMA = Schema({'vid': int, 
   'properties': DynamicDictionary(unicode, All(_IS_PROPERTY_VALUE, GetDictValue('value'))), 
   'identity-profiles': All([_IDENTITY_PROFILE_SCHEMA], Length(min=1))}, required=True, extra=True)