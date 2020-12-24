# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/navigation_mdp/reward.py
# Compiled at: 2020-04-22 14:18:58
# Size of source mod 2**32: 2472 bytes
import numpy as np

class AbstractStateRewardSpec:

    def __init__(self, key=None, feature_key=None, preprocess_fn=lambda x: x, postprocess_fn=lambda x: x):
        self.key = key
        self.feature_key = key if feature_key is None else feature_key
        self.preprocess_fn = preprocess_fn
        self.postprocess_fn = postprocess_fn

    def __call__(self, state):
        return self.compute_reward(state)

    def get_key(self):
        return self.key

    def get_feature_key(self):
        return self.feature_key

    def compute_reward(self, state):
        raise NotImplementedError

    def reward(self, state):
        return self.compute_reward(state)

    def preprocess(self, features):
        return self.preprocess_fn(features)

    def postprocess(self, reward):
        return self.postprocess_fn(reward)


class RewardStateScalar(AbstractStateRewardSpec):

    def __init__(self, loc_to_reward_dict, class_id_to_reward_dict, default=0, key=None, feature_key=None, preprocess_fn=lambda x: x, postprocess_fn=lambda x: x):
        super().__init__(key, feature_key, preprocess_fn, postprocess_fn)
        self.loc_to_reward_dict = loc_to_reward_dict
        self.class_id_to_reward_dict = class_id_to_reward_dict
        self.default = default

    def compute_reward(self, state):
        if self.loc_to_reward_dict is not None:
            if state.location in self.loc_to_reward_dict:
                return self.postprocess_fn(self.loc_to_reward_dict[self.preprocess_fn(state.location)])
        if self.class_id_to_reward_dict is not None:
            if state.class_id in self.class_id_to_reward_dict:
                return self.postprocess_fn(self.class_id_to_reward_dict[self.preprocess_fn(state.class_id)])
        return self.postprocess_fn(self.preprocess_fn(self.default))


class RewardStateFeatureModel(AbstractStateRewardSpec):

    def __init__(self, r_model, key=None, feature_key=None, preprocess_fn=lambda x: x, postprocess_fn=lambda x: x):
        super().__init__(key, feature_key, preprocess_fn, postprocess_fn)
        self.r_model = r_model

    def compute_reward(self, state):
        return self.postprocess_fn(self.r_model(self.preprocess_fn(state.get_features(key=(self.get_feature_key())))))