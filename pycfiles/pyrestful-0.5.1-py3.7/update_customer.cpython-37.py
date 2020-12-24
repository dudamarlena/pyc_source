# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/demos/update_customer.py
# Compiled at: 2019-03-02 23:45:23
# Size of source mod 2**32: 1664 bytes
import sys, json
if sys.version_info > (3, ):
    raw_input = input
    import http.client as httplib
    import urllib.parse as urllib
else:
    import httplib, urllib
print('Update customer')
print('===============')
id_customer = raw_input('Id Customer      : ')
name_customer = raw_input('Customer Name    : ')
address_customer = raw_input('Customer Address : ')
if len(id_customer) == 0 and len(name_customer) == 0 and len(address_customer) == 0:
    print('You must indicates id, name and address of customer')
else:
    params = urllib.urlencode({'name_customer':str(name_customer),  'address_customer':str(address_customer)})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn = httplib.HTTPConnection('localhost:8080')
    conn.request('PUT', '/customer/%s' % id_customer, params, headers)
    resp = conn.getresponse()
    data = resp.read()
    if resp.status == 200:
        json_data = json.loads(data.decode('utf-8'))
        print(json_data)
    else:
        print(data.decode('utf-8'))