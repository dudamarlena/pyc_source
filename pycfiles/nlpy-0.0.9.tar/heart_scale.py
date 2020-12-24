# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/dataset/heart_scale.py
# Compiled at: 2014-11-17 02:57:22
from nlpy.dataset import AbstractDataset
from nlpy.util import FeatureContainer, internal_resource
import numpy as np

class HeartScaleDataset(AbstractDataset):

    def __init__(self, target_format=None):
        super(HeartScaleDataset, self).__init__(target_format)
        feature = FeatureContainer(internal_resource('dataset/heart_scale.txt'))
        self.data = feature.data
        self.targets = feature.targets
        self._target_size = 2

    def train_set(self):
        return [
         (
          self.data[:150], np.array(map(self._target_map, self.targets[:150])))]

    def valid_set(self):
        return [
         (
          self.data[150:200], np.array(map(self._target_map, self.targets[150:200])))]

    def test_set(self):
        return [
         (
          self.data[200:], np.array(map(self._target_map, self.targets[200:])))]