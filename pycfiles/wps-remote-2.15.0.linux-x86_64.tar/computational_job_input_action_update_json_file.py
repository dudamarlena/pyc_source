# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computational_job_input_action_update_json_file.py
# Compiled at: 2016-02-23 09:09:50
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import json, path, computational_job_input_action

class ComputationalJobInputActionUpdateJSONFile(computational_job_input_action.ComputationalJobInputAction):

    def __init__(self, input_ref, target_json_file, json_path_expr, source_template_json_file):
        super(ComputationalJobInputActionUpdateJSONFile, self).__init__()
        self._input_ref = input_ref
        self._target_json_file = target_json_file if isinstance(target_json_file, path.path) else path.path(target_json_file)
        self.jsonpath_expr = json_path_expr
        self._config_file_template = source_template_json_file if isinstance(source_template_json_file, path.path) else path.path(source_template_json_file)

    def set_inputs(self, inputs):
        if self._input_ref in inputs.names():
            if not self.exists() and self._config_file_template != None:
                self._config_file_template.copyfile(self._target_json_file)
                self.update_file(inputs)
            elif not self.exists() and self._config_file_template == None:
                raise Exception('Cannot find target JSON file ' + str(self._target_json_file))
            else:
                self.update_file(inputs)
        return

    def update_file(self, inputs):
        json_text = self._target_json_file.text()
        j = json.loads(json_text)
        exec 'j' + self.jsonpath_expr + '=' + str(inputs[self._input_ref].get_value_as_JSON_literal())
        json.dump(j, self._target_json_file.open('w'), indent=4)

    def exists(self):
        return self._target_json_file.exists()