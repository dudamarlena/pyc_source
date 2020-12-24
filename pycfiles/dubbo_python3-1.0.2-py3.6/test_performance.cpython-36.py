# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_performance.py
# Compiled at: 2020-04-20 23:48:48
# Size of source mod 2**32: 4450 bytes
"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

"""
import pstats
from jsonrpcclient.clients.http_client import HTTPClient
from dubbo_client import ZookeeperRegistry, DubboClient
number = 1000

def test_client_every_new():
    for x in range(number):
        url = 'http://{0}{1}'.format('172.19.3.111:38080/', 'com.ofpay.demo.api.UserProvider')
        client = HTTPClient(url)
        response = client.request('getUser', 'A003')
        response2 = client.request('queryUser', {'age':18,  'time':1428463514153,  'sex':'MAN',  'id':'A003',  'name':'zhangsan'})
        response3 = client.request('isLimit', 'MAN', 'Joe')
        response4 = client.request('getUser', 'A005')


def test_client():
    url = 'http://{0}{1}'.format('172.19.3.111:38080/', 'com.ofpay.demo.api.UserProvider')
    client = HTTPClient(url)
    for x in range(number):
        response = client.request('getUser', 'A003')
        response2 = client.request('queryUser', {'age':18, 
         'time':1428463514153,  'sex':'MAN',  'id':'A003',  'name':'zhangsan'})
        response3 = client.request('isLimit', 'MAN', 'Joe')
        response4 = client.request('getUser', 'A005')


def test_dubbo():
    service_interface = 'com.ofpay.demo.api.UserProvider'
    registry = ZookeeperRegistry('172.19.65.33:2181')
    user_provider = DubboClient(service_interface, registry, version='2.0')
    for x in range(number):
        user_provider.getUser('A003')
        user_provider.queryUser({'age':18, 
         'time':1428463514153,  'sex':'MAN',  'id':'A003',  'name':'zhangsan'})
        user_provider.isLimit('MAN', 'Joe')
        user_provider('getUser', 'A005')


if __name__ == '__main__':
    p = pstats.Stats('test_dubbo.txt')
    p.sort_stats('time').print_stats()
    np = pstats.Stats('test_client_every_new.txt')
    np.sort_stats('time').print_stats()
    cp = pstats.Stats('test_client.txt')
    cp.sort_stats('time').print_stats()