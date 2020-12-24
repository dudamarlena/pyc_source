# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cluster_drug_discovery/input_preprocess/point.py
# Compiled at: 2019-09-30 06:39:48
# Size of source mod 2**32: 233 bytes


class Point(object):

    def __init__(self, value, epoch, traj, model):
        self.value = value
        self.epoch = epoch
        self.traj = traj
        self.model = model

    def retrieve_struct(self):
        pass