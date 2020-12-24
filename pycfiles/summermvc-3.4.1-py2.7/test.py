# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/test.py
# Compiled at: 2018-05-31 04:41:12
import requests
r = requests.get('http://127.0.0.1:8081/get/user/30000?format=json')
print r.status_code
print r.headers
print r.content
print '=========='
r = requests.get('http://127.0.0.1:8081/get/user?userid=10000&format=xml')
print r.status_code
print r.headers
print r.content
print '=========='
r = requests.get('http://127.0.0.1:8081/file/not/found')
print r.status_code
print r.headers
print r.content
print '=========='
r = requests.get('http://127.0.0.1:8081/chunk')
print r.status_code
print r.headers
print r.content
print '=========='
r = requests.get('http://127.0.0.1:8081/redirect')
print r.status_code
print r.headers
print r.content
print '=========='
r = requests.get('http://127.0.0.1:8081/internal/redirect')
print r.status_code
print r.headers
print r.content