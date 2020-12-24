# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computation_job_param.py
# Compiled at: 2018-09-14 04:56:37
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import computation_job_input

class ComputationJobParam(computation_job_input.ComputationJobInput):

    def __init__(self, name, input_type, title, descr, default=None, formatter=None, min_occurencies=0, max_occurencies=1, input_mime_type=None):
        super(ComputationJobParam, self).__init__(name, input_type, title, descr, default, formatter, input_mime_type)
        self._min = min_occurencies
        self._max = max_occurencies

    def validate(self):
        if not (self._min <= len(self._value) and len(self._value) <= self._max):
            raise TypeError('Actual value for parameter has wrong multiplicity')
        return super(ComputationJobParam, self).validate()