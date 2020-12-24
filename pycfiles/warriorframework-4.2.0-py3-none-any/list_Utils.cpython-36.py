# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/Framework/Utils/list_Utils.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 2050 bytes
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

def get_list_by_separating_strings(list_to_be_processed, char_to_be_replaced=',', str_to_replace_with_if_empty=None):
    """ This function converts a list of type:
     ['str1, str2, str3', 'str4, str5, str6, str7', None, 'str8'] to:
     [['str1', 'str2', 'str3'], ['str4', 'str5', 'str6', 'str7'], [], ['str8']]
    """
    final_list = []
    if list_to_be_processed is not None:
        if list_to_be_processed is not False:
            if list_to_be_processed != '':
                for i in range(0, len(list_to_be_processed)):
                    if list_to_be_processed[i] is None or list_to_be_processed[i] is False or list_to_be_processed[i] == '':
                        temp_list = []
                    else:
                        if list_to_be_processed[i] == '':
                            list_to_be_processed[i] = str_to_replace_with_if_empty
                        temp_list = list_to_be_processed[i].split(char_to_be_replaced)
                        for j in range(0, len(temp_list)):
                            temp_list[j] = temp_list[j].strip()

                    final_list.append(temp_list)

    return final_list


def get_list_comma_sep_string(input_string):
    """
    This function converts a comma separated string in to a list

     Eg: "a, b, c, d, e, f" would become ['a', 'b', 'c', 'd', 'e', 'f']
    """
    final_list = input_string.split(',')
    for i in range(0, len(final_list)):
        final_list[i] = final_list[i].strip()

    return final_list