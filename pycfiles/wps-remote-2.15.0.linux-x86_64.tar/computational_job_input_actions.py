# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computational_job_input_actions.py
# Compiled at: 2016-02-23 09:09:48
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
from collections import OrderedDict
import path, computational_job_input_action_cmd_param, computational_job_input_action_create_json_file, computational_job_input_action_update_json_file, computational_job_input_action_copyfile, computational_job_input_action_update_ini_file

class ComputationalJobInputActions(object):

    @staticmethod
    def create_from_config(input_sections):
        """Create a InputParameters object.

        input_sections: a dictionary such as { action1 : [( 'par1_input1_name' , par1_input1_value ), ( 'par2_input1_name' , par2_input1_value ), ...], action2 : [ .... ], ... }
        """
        input_sections_reshaped = OrderedDict()
        for k in sorted(input_sections):
            d = dict(input_sections[k])
            input_sections_reshaped[k] = d

        return ComputationalJobInputActions.create_from_dict(input_sections_reshaped)

    @staticmethod
    def create_from_dict(input_action_def_dict):
        """Create a input parameters set from a definitions

        paremeters_types_defs is a dictionary such as {input_ref1 : { 'action1_attrubute1_name' : action1_attrubute1_value, ... }, input_ref2 : { 'action2_attrubute1_name' : action2_attrubute1_value, ... }, ... }
        """
        cja = ComputationalJobInputActions()
        action2add = None
        for action_section_name, d in OrderedDict(input_action_def_dict).items():
            if 'class' in d:
                if d['class'] == 'cmdline':
                    alias = d['alias'] if 'alias' in d else None
                    action2add = computational_job_input_action_cmd_param.ComputationalJobInputActionCmdParam(d['input_ref'], d['template'], alias=alias)
                elif d['class'] == 'createJSONfile':
                    json_path_expr = d['json_path_expr'] if 'json_path_expr' in d else None
                    action2add = computational_job_input_action_create_json_file.ComputationalJobInputActionCreateJSONFile(d['input_ref'], d['target_filepath'], json_path_expr, path.path(d['json_schema']))
                elif d['class'] == 'updateJSONfile':
                    action2add = computational_job_input_action_update_json_file.ComputationalJobInputActionUpdateJSONFile(d['input_ref'], d['target_filepath'], d['json_path_expr'], d['source_filepath'])
                elif d['class'] == 'copyfile':
                    action2add = computational_job_input_action_copyfile.ComputationalJobInputActionCopyFile(d['source_filepath'], d['target_filepath'])
                elif d['class'] == 'updateINIfile':
                    alias = d['alias'] if 'alias' in d else None
                    action2add = computational_job_input_action_update_ini_file.ComputationalJobInputActionUpdateINIFile(d['input_ref'], d['source_filepath'], d['target_filepath'], d['section'], alias)
                elif d['class'] == 'updateINIfileList':
                    alias = d['alias'] if 'alias' in d else None
                    action2add = computational_job_input_action_update_ini_file.ComputationalJobInputActionUpdateINIFileAsList(d['input_ref'], d['source_filepath'], d['target_filepath'], d['section'], alias)
                else:
                    raise TypeError('Unknown class value ' + str(d['class']) + ' for action related to input ' + str(d['input_ref']))
            else:
                raise TypeError('Cannot create computational job action related to input ' + str(d['input_ref']) + ' without attribute class')
            cja.add_actions(action2add)

        return cja

    def __init__(self):
        self._actions = []

    def get_cmd_line(self):
        cmd_line = ''
        for a in self._actions:
            if a.can_produce_cmd_line():
                cmd_line += ' ' + a.get_cmd_line()

        return cmd_line.lstrip()

    def execute(self, input_values):
        for a in self._actions:
            a.set_inputs(input_values)

    def add_actions(self, a):
        self._actions.append(a)