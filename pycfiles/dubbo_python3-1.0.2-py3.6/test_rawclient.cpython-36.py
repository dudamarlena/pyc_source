# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_rawclient.py
# Compiled at: 2020-04-20 23:48:48
# Size of source mod 2**32: 1124 bytes
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
from jsonrpcclient.clients.http_client import HTTPClient

def test_client_every_new():
    url = 'http://{0}{1}'.format('zookeeper:38081/', 'com.ofpay.demo.api.UserProvider2')
    client = HTTPClient(url)
    response = client.request('getUser', 'A003')
    print(response)


if __name__ == '__main__':
    test_client_every_new()