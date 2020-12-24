# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/ProductDrivers/common_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 1176 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
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
from warrior.WarriorCore import kw_driver
import warrior.Actions.CommonActions

def main(keyword, data_repository, args_repository):
    """Import all actions related to common driver and call the driver Utils
    to execute a keyword """
    package_list = [
     warrior.Actions.CommonActions]
    return kw_driver.execute_keyword(keyword, data_repository, args_repository, package_list)