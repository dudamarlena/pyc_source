# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computation_job_const.py
# Compiled at: 2016-02-23 09:10:20
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import computation_job_input

class ComputationJobConst(computation_job_input.ComputationJobInput):

    def __init__(self, name, input_type, title, descr, value):
        super(ComputationJobConst, self).__init__(name, input_type, title, descr)
        self.set_value(value)