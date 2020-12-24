# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\lib\loadjson.py
# Compiled at: 2018-09-18 04:40:01
import json
data = '{"a" : 1,"b" : 2, "c" : 3, "d" : 4,"e" : 5 }'
json1 = json.loads(data)
print json1['c']
keys = json1.keys()
print '-------------------'
for aj_key in json1.keys():
    print aj_key

print '-------------------'
print json1