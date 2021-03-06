# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/Classes/argument_datatype_class.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 5048 bytes
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
import ast, traceback
from io import IOBase
from warrior.Framework.Utils.print_Utils import print_error, print_info, print_warning
from warrior.Framework.Utils import config_Utils, file_Utils

class ArgumentDatatype(object):
    __doc__ = 'This is the class that gets the data type of an argument\n    supplied by the user and stores it in the data repository.\n    '
    type_funcs = {'str':str,  'int':int, 
     'float':float, 
     'bool':bool, 
     'list':list, 
     'tuple':tuple, 
     'dict':dict, 
     'file':IOBase}

    def __init__(self, arg_name, arg_value):
        """Constructor that gets the arg_name and arg_value """
        self.arg_name = arg_name
        self.arg_value = arg_value
        self.datatype = None

    def get_type_func(self, datatype='str'):
        """get the function to do the type conversion
        """
        return self.type_funcs[datatype]

    def convert_arg_to_datatype(self):
        """Parses the input argument to find the data type requested by the user

        This is based on the starting letters of the argument name
        If arg_name starts with:
        1. str_ = string
        2. int_ = integer
        3. float_ = float
        4. bool_ = boolean
        5. list_ = list
        6. tuple_ = tuple
        7. dict_ = dict

        Default: if none of the above naming convention matches then the argument value
        will be treated as a string
        """
        self.datatype = None
        if self.arg_name.startswith('str_'):
            return self.arg_value
        else:
            if self.arg_name.startswith('int_'):
                self.datatype = int
            else:
                if self.arg_name.startswith('float_'):
                    self.datatype = float
                else:
                    if self.arg_name.startswith('bool_'):
                        self.datatype = bool
                        if self.arg_value.lower() == 'true':
                            self.arg_value = 'True'
                        else:
                            if self.arg_value.lower() == 'false':
                                self.arg_value = 'False'
                    else:
                        if self.arg_name.startswith('list_'):
                            self.datatype = list
                        else:
                            if self.arg_name.startswith('tuple_'):
                                self.datatype = tuple
                            else:
                                if self.arg_name.startswith('dict_'):
                                    self.datatype = dict
                                elif self.arg_name.startswith('file_'):
                                    self.datatype = IOBase
                                    tc_path = config_Utils.tc_path
                                    fname = file_Utils.getAbsPath(self.arg_value, tc_path)
                                    try:
                                        self.arg_value = open(fname)
                                    except IOError:
                                        print_warning('given file {} does not exist, please check, it should be relative to testcase path {}'.format(fname, tc_path))

                                else:
                                    return self.arg_value
            if self.datatype is not None:
                convert_msg = 'Input argument {0} will be converted to a {1}'.format(self.arg_name, self.datatype)
                print_info(convert_msg)
            result = self.convert_string_to_datatype()
            return result

    def convert_string_to_datatype(self):
        """Converts an input string to a python datatype """
        err_msg = "\nUser input argument value {0} does not match python syntax for '{1}'".format(self.arg_value, self.datatype)
        info_msg = 'Warrior FW will handle user input argument value as string (default)\n'
        result = self.arg_value
        try:
            if self.datatype is not IOBase:
                result = ast.literal_eval(self.arg_value)
        except Exception:
            print_error(err_msg)
            print_info(info_msg)
            print_error('unexpected error: {0}'.format(traceback.format_exc()))
            result = self.arg_value
        else:
            if self.datatype is not IOBase:
                if not isinstance(result, self.datatype):
                    print_error(err_msg)
                    print_info(info_msg)
                    result = self.arg_value
            return result