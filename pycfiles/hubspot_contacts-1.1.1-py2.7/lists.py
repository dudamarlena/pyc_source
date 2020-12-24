# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hubspot/contacts/_schemas/lists.py
# Compiled at: 2017-11-13 03:36:59
from voluptuous import Schema
CONTACT_LIST_SCHEMA = Schema({'listId': int, 'name': unicode, 'dynamic': bool}, required=True, extra=True)
CONTACT_LIST_MEMBERSHIP_UPDATE_SCHEMA = Schema({'updated': list}, required=True, extra=True)