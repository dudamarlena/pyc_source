# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hubspot/contacts/_property_utils.py
# Compiled at: 2017-11-13 03:15:10
from hubspot.contacts.properties import get_all_properties

def get_property_type_by_property_name(connection):
    property_definitions = get_all_properties(connection)
    property_type_by_property_name = {p.name:type(p) for p in property_definitions}
    return property_type_by_property_name