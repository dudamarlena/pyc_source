# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/janrain/retrieve_data.py
# Compiled at: 2013-06-20 04:08:17
"""
Reference and playing around with the janrain api
"""
import requests, sys, pprint
try:
    import simplejson as json
except ImportError:
    import json

try:
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

client_id = 'qvufhhghk4ccgrbqcq8cap2rm6p6kgnz'
client_secret = 'v5b9srfzsnd7wnrpq2zv4mdyete6js8q'
janrain_url = 'https://kagiso.dev.janraincapture.com'
api_call = 'entity.count'
type_name = 'user'
payload = {'client_id': client_id, 'client_secret': client_secret, 
   'type_name': type_name}
response = requests.post('%s/%s' % (janrain_url, api_call), data=payload)
print response
try:
    pprint.pprint(response.json())
except:
    pprint.pprint(response.content)

api_call = 'entity.create'
user_attributes = {'givenName': 'Bob', 'familyName': 'Smith'}
print json.dumps(user_attributes)
payload['attributes'] = json.dumps(user_attributes)
response = requests.post('%s/%s' % (janrain_url, api_call), data=payload)
print response.content
import pdb
pdb.set_trace()
sys.exit()