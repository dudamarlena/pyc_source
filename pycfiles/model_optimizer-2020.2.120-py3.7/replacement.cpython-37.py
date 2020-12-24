# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/middle/replacement.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 1208 bytes
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
from mo.utils import class_registration
from mo.utils.replacement_pattern import ReplacementPattern

class MiddleReplacementPattern(ReplacementPattern):
    registered_ops = {}
    registered_cls = []

    def run_after(self):
        from extensions.middle.pass_separator import MiddleStart
        return [
         MiddleStart]

    def run_before(self):
        from extensions.middle.pass_separator import MiddleFinish
        return [
         MiddleFinish]

    @classmethod
    def class_type(cls):
        return class_registration.ClassType.MIDDLE_REPLACER


ReplacementPattern.excluded_replacers.append(MiddleReplacementPattern)