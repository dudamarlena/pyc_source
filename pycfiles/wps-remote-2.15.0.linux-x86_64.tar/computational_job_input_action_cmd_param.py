# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computational_job_input_action_cmd_param.py
# Compiled at: 2016-02-23 09:10:06
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import copy, computational_job_input_action

class ComputationalJobInputActionCmdParam(computational_job_input_action.ComputationalJobInputAction):

    def __init__(self, input_ref, template='--name=value', alias=None):
        super(ComputationalJobInputActionCmdParam, self).__init__()
        self._input_ref = input_ref
        self._template = template
        self._cmdline = ''
        self._alias = alias

    def set_inputs(self, inputs):
        if self._input_ref in inputs.names():
            self._cmdline += ' ' + self._instance_template(self._input_ref, inputs[self._input_ref].get_value_string())
        self._cmdline = self._cmdline.strip()

    def _instance_template(self, name, value_str):
        cmd = ''
        if self._alias != None:
            name = self._alias
        hasName = False
        hasValue = False
        template = copy.deepcopy(self._template)
        if 'name' in template:
            template = template.replace('name', '%s')
            hasName = True
        if 'value' in self._template:
            template = template.replace('value', '%s')
            hasValue = True
        if hasName and hasValue:
            cmd += template % (name, value_str)
        elif hasName:
            cmd += template % name
        elif hasValue:
            cmd += template % value_str
        else:
            raise Exception('Bad template for command line parameter ' + name)
        return cmd

    def get_cmd_line(self):
        return self._cmdline