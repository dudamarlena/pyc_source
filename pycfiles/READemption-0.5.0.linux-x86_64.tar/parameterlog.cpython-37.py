# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/parameterlog.py
# Compiled at: 2019-07-15 11:59:22
# Size of source mod 2**32: 596 bytes


class ParameterLog(object):

    def __init__(self, log_file):
        self.log_file = log_file
        self.delimiter = ': '


class ParameterLogger(ParameterLog):

    def add_paramter(self, parameter, value):
        log_fh = open(self.log_file, 'a')
        log_fh.write(self.delimiter.join([parameter, value]) + '\n')
        log_fh.close()


class ParameterLogReader(ParameterLog):

    def read_parameters(self):
        parameters = {}
        for line in open(self.log_file):
            paramter, value = line[:-1].split(self.delimiter)
            parameters[parameters] = value