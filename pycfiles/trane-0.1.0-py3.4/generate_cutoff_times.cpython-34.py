# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/trane/utils/generate_cutoff_times.py
# Compiled at: 2018-04-12 10:25:16
# Size of source mod 2**32: 2349 bytes
import numpy as np
__all__ = [
 'CutoffTimeBase', 'ConstantCutoffTime', 'DynamicCutoffTime']

class CutoffTimeBase:

    def __init__(self):
        pass

    def generate_cutoffs(self, entity_to_data_dict, time_column):
        entity_to_data_and_cutoff_dict = {}
        for entity in entity_to_data_dict:
            entity_data = entity_to_data_dict[entity]
            entity_training_cutoff, entity_label_cutoff = self.get_cutoff(entity_data, time_column)
            entity_to_data_and_cutoff_dict[entity] = (
             entity_data, entity_training_cutoff, entity_label_cutoff)

        return entity_to_data_and_cutoff_dict


class ConstantCutoffTime(CutoffTimeBase):

    def __init__(self, training_cutoff, label_cutoff):
        self.training_cutoff = training_cutoff
        self.label_cutoff = label_cutoff

    def get_cutoff(self, entity_data, time_column):
        return (
         self.training_cutoff, self.label_cutoff)


class DynamicCutoffTime(CutoffTimeBase):
    __doc__ = '\n    DynamicCutoffTime use (1 - training_ratio - label_ratio) * N records \n    to generate features.\n    use the following training_ratio * N records for training labels.\n    use the last label_ratio * N records for testing labels.\n    '

    def __init__(self, training_ratio=0.2, label_ratio=0.2):
        assert training_ratio + label_ratio < 1
        assert training_ratio > 0 and label_ratio > 0
        self.training_ratio = training_ratio
        self.label_ratio = label_ratio

    def get_cutoff(self, entity_data, time_column):
        timestemps = entity_data[time_column].copy()
        timestemps = timestemps.sort_values()
        N = len(timestemps)
        n_label = int(np.ceil(N * self.label_ratio))
        n_training_label = int(np.ceil(N * (self.training_ratio + self.label_ratio)))
        n_feature = N - n_training_label
        n_training = n_training_label - n_label
        return (timestemps.iloc[n_feature], timestemps.iloc[(n_feature + n_training)])