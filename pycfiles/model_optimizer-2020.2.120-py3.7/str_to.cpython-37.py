# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/utils/str_to.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1276 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

class StrTo(object):

    @staticmethod
    def tuple(type_of_elements: type, string: str):
        if type_of_elements == int:
            string = string.replace('L', '')
        return tuple((type_of_elements(x) for x in string[1:-1].split(',') if x != ''))

    @staticmethod
    def list(string: str, type_of_elements: type, sep: str):
        result = string.split(sep)
        result = [type_of_elements(x) for x in result]
        return result

    @staticmethod
    def bool(val: str):
        if val.lower() == 'false':
            return False
        if val.lower() == 'true':
            return True
        raise ValueError('Value is not boolean: ' + val)