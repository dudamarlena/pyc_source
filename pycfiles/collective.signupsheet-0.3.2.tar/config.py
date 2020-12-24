# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/signableevent/config.py
# Compiled at: 2011-07-29 07:55:08
__doc__ = 'Common configuration constants\n'
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