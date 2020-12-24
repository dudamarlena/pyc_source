# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/lems/sim/recording.py
# Compiled at: 2015-11-16 08:17:20
__doc__ = '\nRecording class(es).\n\n@author: Gautham Ganapathy\n@organization: LEMS (http://neuroml.org/lems/, https://github.com/organizations/LEMS)\n@contact: gautham@lisphacker.org\n'
from lems.base.base import LEMSBase

class Recording(LEMSBase):
    """
    Stores details of a variable recording across a single simulation run.
    """

    def __init__(self, variable, full_path, data_output, recorder):
        self.variable = variable
        self.full_path = full_path
        self.data_output = data_output
        self.recorder = recorder
        self.values = []

    def __str__(self):
        return ('Recording: {0} ({1}), {2}, size: {3}').format(self.variable, self.full_path, self.recorder, len(self.values))

    def __repr__(self):
        return self.__str__()

    def add_value(self, time, value):
        self.values.append((time, value))