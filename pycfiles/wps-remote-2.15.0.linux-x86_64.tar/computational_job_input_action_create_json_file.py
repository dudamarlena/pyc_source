# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computational_job_input_action_create_json_file.py
# Compiled at: 2018-09-27 07:00:49
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import json, path, computational_job_input_action, logging, jsonschema

class ComputationalJobInputActionCreateJSONFile(computational_job_input_action.ComputationalJobInputAction):

    def __init__(self, input_ref, json_filepath, json_path_expr=None, json_schema=None):
        super(ComputationalJobInputActionCreateJSONFile, self).__init__()
        self._input_ref = input_ref
        self._json_filepath = json_filepath if isinstance(json_filepath, path.path) else path.path(json_filepath)
        self._json_path_expr = json_path_expr
        self.json_files_created = []
        if isinstance(json_schema, path.path):
            self._json_schema = json.loads(json_schema.text())
        else:
            self._json_schema = json.loads(json_schema)

    def set_inputs(self, inputs):
        logger = logging.getLogger('ComputationalJobInputActionCreateJSONFile.set_inputs')
        logger.debug('start creating JSON file')
        if self._input_ref in inputs.names():
            text2write = inputs[self._input_ref].get_value()
            if type(text2write) == list:
                logger.debug('a list of asset is given, iterate over json texts')
                for single_json_text in text2write:
                    if self.validate_json(single_json_text):
                        self.create_json_file(single_json_text)

            elif type(text2write) != list:
                logger.debug('only one json string is give, just write the file with the value of the json path expr')
                if self.validate_json(text2write):
                    self.create_json_file(text2write)
            else:
                msg = 'Cannot produce JSON file with current configuration and input in ComputationalJobInputActionCreateJSONFile'
                logger.debug(msg)
                raise Exception(msg)

    def validate_json(self, json_text):
        logger = logging.getLogger('ComputationalJobInputActionCreateJSONFile.validate_json')
        if self._json_schema == None:
            logger.warning('cannot validate json input against json schema')
            return True
        else:
            try:
                jsonschema.validate(json_text, self._json_schema)
                return True
            except Exception as ex:
                msg = 'Invalid json for asset: ' + str(ex)
                logger.fatal(msg)
                raise ex

            return

    def create_json_file(self, json_text):
        json_filepath = self._extract_id_from_json(json_text)
        fp = json_filepath.open('w')
        json.dump(json_text, fp)
        fp.close()
        self.json_files_created.append(json_filepath)

    def _extract_id_from_json(self, json_text):
        if self._json_path_expr != None and self._json_path_expr != '':
            _id = eval('json_text' + self._json_path_expr)
            self._json_filepath = str(self._json_filepath).replace('${json_path_expr}', '%i')
            fp = self._json_filepath % _id
        else:
            fp = self._json_filepath
        return path.path(fp)

    def exists(self):
        files_exists = map(lambda fp: fp.exists(), self.json_files_created)
        files_exists = list(set(files_exists))
        return len(files_exists) == 1 and files_exists[0]