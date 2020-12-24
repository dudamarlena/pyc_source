# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_rpclib.py
# Compiled at: 2020-04-20 23:48:48
# Size of source mod 2**32: 2091 bytes
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
import time
from dubbo_client import ZookeeperRegistry, DubboClient, DubboClientError, ApplicationConfig
__author__ = 'caozupeng'
if __name__ == '__main__':
    config = ApplicationConfig('test_rpclib')
    service_interface = 'com.ofpay.demo.api.UserProvider'
    registry = ZookeeperRegistry('115.28.74.185:2181', config)
    user_provider = DubboClient(service_interface, registry, version='2.0')
    for i in range(1000):
        try:
            print(user_provider.getUser('A003'))
        except DubboClientError as client_error:
            print(client_error.message)
            print(client_error.data)

        time.sleep(5)