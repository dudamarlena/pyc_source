# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/navigation_mdp/state.py
# Compiled at: 2020-04-22 00:43:51
# Size of source mod 2**32: 10895 bytes
import itertools, numpy as np

class DiscreteStateSpace:
    __doc__ = ' Discrete State Space specification class\n    Note: Designed to handle any dimensionality but dim > 2 is not tested.\n    '

    def __init__(self, *args):
        self.n_dims = len(args)
        self.limits = args
        self.n_states = np.product(self.limits)
        self.idxs = self._get_idxs()
        self.space = self._get_space()
        self.state_lst, self.loc_to_state_dict, self.state_to_loc_dict, self.loc_to_idx_dict = self._get_states()

    def _get_idxs(self):
        return np.arange(self.n_states).reshape(self.limits)

    def _get_space(self):
        return np.array(list((itertools.product)(*[np.arange(lim) for lim in self.limits]))).reshape(self.limits + (self.n_dims,))

    def _get_states(self):
        state_list = []
        loc_to_state_dict = {}
        state_to_loc_dict = {}
        loc_to_idx_dict = {}
        idx = 0
        for loc in list((itertools.product)(*[np.arange(lim) for lim in self.limits])):
            state = State(location=loc, idx=idx, parent_state_space=self)
            state_list.append(state)
            loc_to_state_dict[loc] = state
            state_to_loc_dict[state] = loc
            loc_to_idx_dict[loc] = idx
            idx += 1

        return (
         state_list, loc_to_state_dict, state_to_loc_dict, loc_to_idx_dict)

    def __str__(self):
        return str(self.space)

    def print_states_meta(self):
        for s in self.state_lst:
            print(s._meta())

    def at_loc(self, loc):
        return self.loc_to_state_dict[loc]

    def __call__(self, idx=None):
        if idx is None:
            return self.state_lst
        return self.__getitem__(idx)

    def __getitem__(self, idx):
        if type(idx) == tuple:
            return self.at_loc(loc=idx)
        return self.state_lst[idx]

    def __len__(self):
        return self.n_states

    def all(self):
        return self.state_lst

    def attach_classes(self, class_ids=[]):
        if len(class_ids) != self.n_states:
            raise Exception('Require class id for each state!')
        self.n_classes = len(np.unique(class_ids))
        for idx, class_id in enumerate(class_ids):
            self.state_lst[idx].attach_class(class_id)

    def sample_and_attach_classes(self, class_ids=[], p_dist=None):
        S = class_ids
        if p_dist is None:
            p_dist = np.ones(len(S)) / len(S)
        if len(p_dist) != len(class_ids):
            raise Exception('class_ids and p_dist must have same length!')
        self.uniq_classes = class_ids
        class_ids = np.random.choice(S, (self.n_states), p=p_dist)
        for idx, class_id in enumerate(class_ids):
            self.state_lst[idx].attach_class(class_id)

    def override_classes_by_loc(self, loc_lst, class_id_lst):
        for i, loc in enumerate(loc_lst):
            self.loc_to_state_dict[loc].attach_class(class_id_lst[i])

        self.uniq_classes = np.unique(self.class_ids)

    @property
    def class_ids(self):
        return np.asarray([self.state_lst[idx].get_class() for idx in range(self.n_states)])

    @property
    def num_classes(self):
        return len(self.uniq_classes)

    def attach_feature_spec(self, PHI_spec, compute=True):
        for state in self.state_lst:
            state.attach_feature_spec(PHI_spec, compute=compute)

    def add_feature_spec_ref(self, key, ref_key):
        for state in self.state_lst:
            state.add_feature_spec_ref(key, ref_key)

    def clear_feature_spec(self):
        for state in self.state_lst:
            state.clear_feature_spec()

    def features(self, loc=None, idx=None, gridded=False, numpyize=True, key=None):
        if loc is not None:
            return np.asarray(self.loc_to_state_dict[loc].get_features(key=key))
        if idx is not None:
            return np.asarray(self.state_lst[idx].get_features(key=key))
        features_lst = [self.state_lst[idx].get_features(key=key) for idx in range(self.n_states)]
        if gridded:
            return np.asarray(features_lst).reshape(self.limits + self.feature_dim(key=key))
        if numpyize:
            return np.asarray(features_lst, dtype=(np.float32))
        return features_lst

    def feature_dim(self, key=None):
        return self.features(idx=0, loc=None, gridded=False, key=key).shape

    def attach_reward_spec(self, R_spec, compute=True):
        for state in self.state_lst:
            state.attach_reward_spec(R_spec, compute=compute)

    def add_reward_spec_ref(self, key, ref_key):
        for state in self.state_lst:
            state.add_reward_spec_ref(key, ref_key)

    def clear_reward_spec(self):
        for state in self.state_lst:
            state.clear_reward_spec()

    def rewards(self, numpyize=True, gridded=False, key=None):
        if gridded:
            rewards = np.asarray([self.state_lst[idx].get_reward(key=key) for idx in range(self.n_states)], dtype=(np.float32))
            return (rewards.reshape)(*self.limits, *(1, ))
        rewards = [self.state_lst[idx].get_reward(key=key) for idx in range(self.n_states)]
        if numpyize:
            return np.asarray(rewards, dtype=(np.float32))
        return rewards

    def set_terminal_status_by_loc(self, loc_lst, b_terminal_status=True):
        for loc in loc_lst:
            self.loc_to_state_dict[loc].set_terminal_status(b_terminal_status)

    def set_terminal_status_by_idx(self, idx_lst, b_terminal_status=True):
        for idx in idx_lst:
            self.state_lst[idx].set_terminal_status(b_terminal_status)

    def get_terminal_states(self):
        return [s for s in self.state_lst if s.terminal_status is True]

    def reset_terminal_status(self):
        for s in self.state_lst:
            s.set_terminal_status(False)

    def _organize_to_grid(self, values):
        return np.asarray(values).reshape(self.shape() + values[0].shape)

    def shape(self):
        return self.limits


class State(object):
    __doc__ = ' State specification class\n    Adapted from https://github.com/david-abel/simple_rl/simple_rl/mdp/StateClass.py\n    '

    def __init__(self, location, idx=None, class_id=None, features=None, reward=None, reward_spec=None, key=None, feature_spec=None, terminal_status=False, parent_state_space=None):
        self.location = location
        self.idx = idx
        self.class_id = class_id
        self.terminal_status = terminal_status
        self.parent_state_space = parent_state_space
        self.features = features
        self.feature_spec_dict = {}
        if feature_spec is not None:
            self.feature_spec_dict[key] = feature_spec
        self.reward = reward
        self.reward_spec_dict = {}
        if reward_spec is not None:
            self.reward_spec_dict[key] = reward_spec

    def is_terminal(self):
        return self.terminal_status

    def set_terminal_status(self, b_terminal_status):
        self.terminal_status = b_terminal_status

    def get_idx(self):
        return self.idx

    def get_id(self):
        return self.location

    def get_location(self):
        return self.location

    def get_class(self):
        return self.class_id

    def attach_class(self, class_id):
        self.class_id = class_id

    def attach_feature_spec(self, feature_spec, compute=True):
        self.feature_spec_dict[feature_spec.get_key()] = feature_spec
        if compute:
            self.compute_features(feature_spec.get_key())

    def add_feature_spec_ref(self, key, ref_key):
        self.feature_spec_dict[ref_key] = self.feature_spec_dict[key]

    def clear_feature_spec(self):
        self.feature_spec_dict = {}

    def attach_reward_spec(self, reward_spec, compute=True):
        self.reward_spec_dict[reward_spec.get_key()] = reward_spec
        if compute:
            self.compute_reward(reward_spec.get_key())

    def add_reward_spec_ref(self, key, ref_key):
        self.reward_spec_dict[ref_key] = self.reward_spec_dict[key]

    def clear_reward_spec(self):
        self.reward_spec_dict = {}

    def get_features(self, key=None, recompute=True):
        if recompute:
            self.compute_features(key=key)
        return self.features

    def get_reward(self, key=None, recompute=True):
        if recompute:
            self.compute_reward(key=key)
        return self.reward

    def compute_reward--- This code section failed: ---

 L. 257         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_reward_spec
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'reward_spec'

 L. 258        10  LOAD_FAST                'reward_spec'
               12  LOAD_CONST               None
               14  COMPARE_OP               is-not
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L. 259        18  LOAD_FAST                'reward_spec'
               20  LOAD_METHOD              compute_reward
               22  LOAD_FAST                'self'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               reward
               30  JUMP_FORWARD         32  'to 32'
             32_0  COME_FROM            30  '30'
             32_1  COME_FROM            16  '16'

Parse error at or near `COME_FROM' instruction at offset 32_0

    def compute_features--- This code section failed: ---

 L. 264         0  LOAD_FAST                'self'
                2  LOAD_METHOD              get_feature_spec
                4  LOAD_FAST                'key'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'feature_spec'

 L. 265        10  LOAD_FAST                'feature_spec'
               12  LOAD_CONST               None
               14  COMPARE_OP               is-not
               16  POP_JUMP_IF_FALSE    32  'to 32'

 L. 266        18  LOAD_FAST                'feature_spec'
               20  LOAD_METHOD              compute_features
               22  LOAD_FAST                'self'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  LOAD_FAST                'self'
               28  STORE_ATTR               features
               30  JUMP_FORWARD         32  'to 32'
             32_0  COME_FROM            30  '30'
             32_1  COME_FROM            16  '16'

Parse error at or near `COME_FROM' instruction at offset 32_0

    def get_reward_spec_names(self):
        return self.reward_spec_dict.keys()

    def get_reward_spec(self, key):
        return self.reward_spec_dict[key]

    def get_feature_spec_names(self):
        return self.feature_spec_dict.keys()

    def get_feature_spec(self, key):
        return self.feature_spec_dict[key]

    def parent_space(self):
        return self.parent_state_space

    def __hash__(self):
        if type(self.location).__module__ == np.__name__:
            return hash(str(self.location))
        if self.location.__hash__ is None:
            return hash(tuple(self.location))
        return hash(self.location)

    def __str__(self):
        return 'State: ' + str(self.location)

    def _meta(self):
        return 'State: ' + str(self.location) + ' [ ' + ('C {} '.format(self.get_class()) if self.get_class() is not None else '') + ('R {:.2f} '.format(self.get_reward()) if self.get_reward() is not None else '') + ('features {} '.format(self.get_features().shape) if self.get_features() is not None else '') + ('Terminal ' if self.is_terminal() else '') + ']'

    def __repr__(self):
        return str(self.__module__) + '.' + self.__class__.__name__ + str(self.location) + ' at ' + hex(id(self))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.location == other.location
        return False

    def __getitem__(self, index):
        return self.location[index]

    def __len__(self):
        return len(self.location)