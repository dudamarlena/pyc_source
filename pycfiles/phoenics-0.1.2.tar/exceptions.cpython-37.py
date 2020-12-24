# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/phoenics/utilities/exceptions.py
# Compiled at: 2019-11-24 12:43:13
# Size of source mod 2**32: 2038 bytes
"""
Licensed to the Apache Software Foundation (ASF) under one or more 
contributor license agreements. See the NOTICE file distributed with this 
work for additional information regarding copyright ownership. The ASF 
licenses this file to you under the Apache License, Version 2.0 (the 
"License"); you may not use this file except in compliance with the 
License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
License for the specific language governing permissions and limitations 
under the License.

The code in this file was developed at Harvard University (2018) and 
modified at ChemOS Inc. (2019) as stated in the NOTICE file.
"""
__author__ = 'Florian Hase'
import sys, traceback

class AbstractError(object):

    def __init__(self, message):
        self.__call__(message)

    def __call__(self, message):
        error_traceback = traceback.format_exc()
        error_traceback = '\n'.join(error_traceback.split('\n')[:-2]) + '\n\n'
        error_type = '\x1b[0;31m%s: %s\x1b[0m\n' % (self.name, message)
        if 'SystemExit' in error_traceback:
            return
        sys.stderr.write(error_traceback)
        sys.stderr.write(error_type)
        sys.exit()


class PhoenicsModuleError(AbstractError):
    name = 'PhoenicsModuleError'


class PhoenicsNotFoundError(AbstractError):
    name = 'PhoenicsNotFoundError'


class PhoenicsParseError(AbstractError):
    name = 'PhoenicsParseError'


class PhoenicsUnknownSettingsError(AbstractError):
    name = 'PhoenicsUnknownSettingsError'


class PhoenicsValueError(AbstractError):
    name = 'PhoenicsValueError'


class PhoenicsVersionError(AbstractError):
    name = 'PhoenicsVersionError'