# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/demos/delete_customer.py
# Compiled at: 2019-03-02 23:45:23
# Size of source mod 2**32: 1290 bytes
import json, sys
if sys.version_info > (3, ):
    raw_input = input
    import http.client as httplib
    import urllib.parse as urllib
else:
    import httplib, urllib
print('Delete customer')
print('===============')
id_customer = raw_input('Id Customer      : ')
if len(id_customer) == 0:
    print('You must indicates id of customer')
else:
    conn = httplib.HTTPConnection('localhost:8080')
    conn.request('DELETE', '/customer/%s' % id_customer)
    resp = conn.getresponse()
    data = resp.read()
    if resp.status == 200:
        json_data = json.loads(data.decode('utf-8'))
        print(json_data)
    else:
        print(data.decode('utf-8'))