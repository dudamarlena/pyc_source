# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/test_config.py
# Compiled at: 2020-04-20 07:09:40
# Size of source mod 2**32: 1278 bytes
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
from dubbo_client import ApplicationConfig

def test_application_config_new():
    application_config = ApplicationConfig('test_app', version='2.0.0', owner='caozupeng', error='ssd')
    if not application_config.architecture == 'web':
        raise AssertionError
    else:
        if not application_config.name == 'test_app':
            raise AssertionError
        else:
            if not application_config.environment == 'run':
                raise AssertionError
            elif not application_config.version == '2.0.0':
                raise AssertionError
            assert 'owner' in application_config.__dict__
        assert 'ssd' not in application_config.__dict__