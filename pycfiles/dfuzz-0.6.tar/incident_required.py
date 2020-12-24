# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/envs/dfuzz/project/dfuzz/dfuzz/tests/dummy/incident_required.py
# Compiled at: 2011-05-04 05:05:05


class Config(object):
    pass


class TargetObj(object):
    code = -11


class Handler(object):

    def __init__(self, cfg, fuzzer):
        self.cfg = cfg
        self.fuzzer = fuzzer

    def handle_failure(self, target_obj, input_file_path, reason):
        self.target_obj = target_obj
        self.input_file_path = input_file_path
        self.reason = reason