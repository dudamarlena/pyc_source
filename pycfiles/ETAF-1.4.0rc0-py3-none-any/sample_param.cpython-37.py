# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/sample_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2738 bytes
from federatedml.param.base_param import BaseParam
import collections

class SampleParam(BaseParam):
    __doc__ = "\n    Define the sample method\n\n    Parameters\n    ----------\n    mode: str, accepted 'random','stratified'' only in this version, specify sample to use, default: 'random'\n\n    method: str, accepted 'downsample','upsample' only in this version. default: 'downsample'\n\n    fractions: None or float or list, if mode equals to random, it should be a float number greater than 0,\n     otherwise a list of elements of pairs like [label_i, sample_rate_i], e.g. [[0, 0.5], [1, 0.8], [2, 0.3]]. default: None\n\n    random_state: int, RandomState instance or None, default: None\n\n    need_run: bool, default True\n        Indicate if this module needed to be run\n    "

    def __init__(self, mode='random', method='downsample', fractions=None, random_state=None, task_type='hetero', need_run=True):
        self.mode = mode
        self.method = method
        self.fractions = fractions
        self.random_state = random_state
        self.task_type = task_type
        self.need_run = need_run

    def check(self):
        descr = 'sample param'
        self.mode = self.check_and_change_lower(self.mode, [
         'random', 'stratified'], descr)
        self.method = self.check_and_change_lower(self.method, [
         'upsample', 'downsample'], descr)
        if self.mode == 'stratified':
            if self.fractions is not None:
                if not isinstance(self.fractions, list):
                    raise ValueError('fractions of sample param when using stratified should be list')
                for ele in self.fractions:
                    if not isinstance(ele, collections.Container) or len(ele) != 2:
                        raise ValueError('element in fractions of sample param using stratified should be a pair like [label_i, rate_i]')

        return True