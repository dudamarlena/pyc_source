# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computational_job_input_action_update_ini_file.py
# Compiled at: 2016-02-23 09:09:56
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import ConfigParser, path, computational_job_input_action

class ComputationalJobInputActionUpdateINIFile(computational_job_input_action.ComputationalJobInputAction):

    def __init__(self, input_ref, source, target, section, alias=None):
        super(ComputationalJobInputActionUpdateINIFile, self).__init__()
        self._input_ref = input_ref
        self._source = source if isinstance(source, path.path) else path.path(source)
        self._target = target if isinstance(target, path.path) else path.path(target)
        self._section = section
        self._alias = alias
        self._value = None
        return

    def set_inputs(self, inputs):
        if self._input_ref in inputs.names():
            self._value = inputs[self._input_ref].get_value()
            if not self.exists() and self._source != None:
                self._source.copyfile(self._target)
                self.update_file(inputs)
            elif not self.exists() and self._source == None:
                raise Exception('Cannot find target INI file ' + str(self._target))
            else:
                self.update_file(inputs)
        return

    def update_file(self, inputs):
        srcINI = ConfigParser.RawConfigParser()
        src = self._target.open()
        srcINI.readfp(src)
        src.close()
        srcINI.set(self._section, self.get_attribute_name(), self._value)
        trg = self._target.open('w')
        srcINI.write(trg)
        trg.close()

    def get_attribute_name(self):
        if self._alias == None:
            return self._input_ref
        else:
            return self._alias

    def exists(self):
        return self._target.exists()


class ComputationalJobInputActionUpdateINIFileAsList(ComputationalJobInputActionUpdateINIFile):

    def __init__(self, input_ref, source, target, section, alias=None):
        super(ComputationalJobInputActionUpdateINIFileAsList, self).__init__(input_ref, source, target, section, alias)

    def update_file(self, inputs):
        srcINI = ConfigParser.RawConfigParser()
        src = self._target.open()
        srcINI.readfp(src)
        src.close()
        json_list_str = (',').join([ '"' + str(token) + '"' for token in self._value.split(',') ])
        srcINI.set(self._section, self.get_attribute_name(), '[' + json_list_str + ']')
        trg = self._target.open('w')
        srcINI.write(trg)
        trg.close()