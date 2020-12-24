# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/front/common/custom_replacement_registry.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 2461 bytes
"""
 Copyright (C) 2017-2020 Intel Corporation

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
import logging as log, os
from mo.utils.custom_replacement_config import parse_custom_replacement_config_file
from mo.utils.error import Error
from mo.utils.utils import refer_to_faq_msg

class CustomReplacementRegistry(object):
    __doc__ = '\n    Registry that contains registered custom calls descriptors.\n    '

    class __CustomReplacementRegistry:

        def __init__(self):
            self.registry = {}

        def __str__(self):
            return repr(self) + str(self.registry)

    def __init__--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              CustomReplacementRegistry
                2  LOAD_ATTR                instance
                4  POP_JUMP_IF_TRUE     18  'to 18'

 L.  39         6  LOAD_GLOBAL              CustomReplacementRegistry
                8  LOAD_METHOD              _CustomReplacementRegistry__CustomReplacementRegistry
               10  CALL_METHOD_0         0  '0 positional arguments'
               12  LOAD_GLOBAL              CustomReplacementRegistry
               14  STORE_ATTR               instance
               16  JUMP_FORWARD         18  'to 18'
             18_0  COME_FROM            16  '16'
             18_1  COME_FROM             4  '4'

Parse error at or near `COME_FROM' instruction at offset 18_0

    def __getattr__(self, name):
        return getattr(self.instance, name)

    instance = None

    def add_custom_replacement_description_from_config(self, file_name: str):
        if not os.path.exists(file_name):
            raise Error("Custom replacement configuration file '{}' doesn't exist. ".format(file_name) + refer_to_faq_msg(46))
        descriptions = parse_custom_replacement_config_file(file_name)
        for desc in descriptions:
            self.registry.setdefault(desc.id, list()).append(desc)
            log.info("Registered custom replacement with id '{}'".format(desc.id))

    def get_custom_replacement_description(self, replacement_id: str):
        if replacement_id in self.registry:
            return self.registry[replacement_id]
        log.warning("Configuration file for custom replacement with id '{}' doesn't exist".format(replacement_id))
        return

    def get_all_replacements_descriptions(self):
        result = list()
        for l in self.registry.values:
            result.extend(l)

        return result