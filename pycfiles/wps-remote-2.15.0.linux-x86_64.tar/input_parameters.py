# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/input_parameters.py
# Compiled at: 2018-09-14 04:50:33
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import introspection
from collections import OrderedDict
import command_line_parameter

class InputParameters(object):

    @staticmethod
    def create_from_config(input_sections):
        """Create a InputParameters object.

            input_sections: a dictionary such as { input1 : [( 'par1_input1_name' , par1_input1_value ), ( 'par2_input1_name' , par2_input1_value ), ...], input2 : [ .... ], ... }
            """
        input_sections_reshaped = OrderedDict()
        for k in sorted(input_sections):
            d = dict(input_sections[k])
            name = d['name']
            del d['name']
            input_sections_reshaped[name] = d

        return InputParameters(input_sections_reshaped)

    def __init__(self, paremeters_types_defs):
        """Create a input parameters set from a definitions

            paremeters_types_defs is a dictionary such as {par1_name : { 'par1_attrubute1_name' : par1_attrubute1_value, ... }, par2_name : { 'par2_attrubute1_name' : par2_attrubute1_value, ... }, ... }
            """
        self._params = OrderedDict()
        for name, d in OrderedDict(paremeters_types_defs).items():
            if 'class' in d:
                try:
                    self._params[name] = introspection.get_class_one_arg(d['class'], name)
                except:
                    raise

            else:
                self._params[name] = command_line_parameter.CommandLineParameter(name)
            self._params[name].inject_values(d)

    def parse(self, input_variables=None):
        """if input_variables is None all params are of type CommandLineParameterConst and input data is read from config file"""
        for n, v in input_variables.items():
            if n in self._params.keys():
                self._params[n].set_actual_value(v)

        self.validate()

    def validate(self):
        for k in self._params.keys():
            self._params[k].validate()

    def get_cmd_line(self):
        cmd_line = ''
        for k in self._params.keys():
            c = self._params[k].get_cmd_line()
            if c != None:
                cmd_line += c

        return cmd_line

    def as_DLR_protocol(self):
        res = []
        for k in self._params.keys():
            n = self._params[k].get_name_no_alias()
            j = self._params[k].as_json_string()
            res.append((n, j))

        return res

    def checkForCodeInsertion(self, argList):
        """ Check user input for bad code insertion
            
                @param argList: user arguments
                @return: False if bad code found, else True
            """
        maliciousCommands = [
         '>', '<', '>>', '|', '>&', '<&']
        maliciousCode = [
         'eval(', 'exec(', 'execfile(', 'input(']
        if any(e in maliciousCommands for e in argList):
            raise IOError('Found bad code in user input')
        for element in argList:
            for code in maliciousCode:
                if code in element:
                    raise IOError('Found bad code in user input')