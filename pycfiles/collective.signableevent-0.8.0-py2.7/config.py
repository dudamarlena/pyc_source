# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/config.py
# Compiled at: 2011-07-29 07:55:08
"""Common configuration constants
"""
PROJECT_NAME = 'collective.signableevent'
ADD_PERMISSIONS = {'EventSignup': 'collective.signableevent: Add EventSignup', 
   'SignableEvent': 'collective.signableevent: Add SignableEvent'}
SKINS_DIR = 'skins'
GLOBALS = globals()
CONFIGLETS = (
 {'id': 'signableevents', 'name': 'Export CSV', 
    'action': 'signableevents_allsigned_csv', 
    'condition': '', 
    'category': 'Products', 
    'visible': 1, 
    'appId': PROJECT_NAME, 
    'permission': 'Manage portal', 
    'imageUrl': 'event_signup_icon.png'},)