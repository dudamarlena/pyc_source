# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computational_job_input_action_copyfile.py
# Compiled at: 2016-02-23 09:10:04
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import path, computational_job_input_action

class ComputationalJobInputActionCopyFile(computational_job_input_action.ComputationalJobInputAction):

    def __init__(self, source, target):
        super(ComputationalJobInputActionCopyFile, self).__init__()
        self._source = source if isinstance(source, path.path) else path.path(source)
        self._target = target if isinstance(target, path.path) else path.path(target)

    def set_inputs(self, inputs):
        self._source.copyfile(self._target)