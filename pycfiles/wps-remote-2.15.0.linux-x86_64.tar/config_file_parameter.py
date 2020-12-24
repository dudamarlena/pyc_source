# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/config_file_parameter.py
# Compiled at: 2016-02-23 09:09:44
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import json, string, path, input_parameters, input_parameter

class ConfigFileParameter(input_parameter.InputParameter):

    def __init__(self, name):
        input_parameter.InputParameter.__init__(self, name)
        self._filepath = None
        return

    def inject_values(self, paremeters_types_defs):
        super(ConfigFileParameter, self).inject_values(paremeters_types_defs)
        self._filepath = path.path(self._filepath)

    def get_cmd_line(self):
        self.update_file()
        return ' '

    def update_file(self):
        pass