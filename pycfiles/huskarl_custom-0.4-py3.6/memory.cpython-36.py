# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/huskarl/memory.py
# Compiled at: 2019-06-13 12:59:36
# Size of source mod 2**32: 6922 bytes
from collections import namedtuple, deque
import random, numpy as np
Transition = namedtuple('Transition', ['state', 'action', 'reward', 'next_state'])

class Memory:
    __doc__ = 'Abstract base class for all implemented memories.\n\n\tDo not use this abstract base class directly but instead use one of the concrete memories implemented.\n\n\tA memory stores interaction sequences between an agent and one or multiple environments.\n\tTo implement your own memory, you have to implement the following methods:\n\t'

    def put(self, *args, **kwargs):
        raise NotImplementedError()

    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


def unpack(traces):
    """Returns states, actions, rewards, end_states, and a mask for episode boundaries given traces."""
    states = [t[0].state for t in traces]
    actions = [t[0].action for t in traces]
    rewards = [[e.reward for e in t] for t in traces]
    end_states = [t[(-1)].next_state for t in traces]
    not_done_mask = [[1 if n.next_state is not None else 0 for n in t] for t in traces]
    return (states, actions, rewards, end_states, not_done_mask)


class OnPolicy(Memory):
    __doc__ = 'Stores multiple steps of interaction with multiple environments.'

    def __init__(self, steps=1, instances=1):
        self.buffers = [[] for _ in range(instances)]
        self.steps = steps
        self.instances = instances

    def put(self, transition, instance=0):
        """Stores transition into the appropriate buffer."""
        self.buffers[instance].append(transition)

    def get(self):
        """Returns all traces and clears the memory."""
        traces = [list(tb) for tb in self.buffers]
        self.buffers = [[] for _ in range(self.instances)]
        return unpack(traces)

    def __len__(self):
        """Returns the number of traces stored."""
        return sum([len(b) - self.steps + 1 for b in self.buffers])


class ExperienceReplay:
    __doc__ = "Stores interaction with an environment as a double-ended queue of Transition instances.\n\t\n\tProvides efficient sampling of multistep traces.\n\tIf exclude_boundaries==True, then traces are sampled such that they don't include episode boundaries.\n\t"

    def __init__(self, capacity, steps=1, exclude_boundaries=False):
        """
                Args:
                        capacity (int): The maximum number of traces the memory should be able to store.
                        steps (int): The number of steps (transitions) each sampled trace should include.
                        exclude_boundaries (bool): If True, sampled traces will not include episode boundaries.
                """
        self.traces = deque(maxlen=capacity)
        self.buffer = []
        self.capacity = capacity
        self.steps = steps
        self.exclude_boundaries = exclude_boundaries

    def put(self, transition):
        """Adds transition to memory."""
        self.buffer.append(transition)
        if len(self.buffer) < self.steps:
            return
        self.traces.append(tuple(self.buffer))
        if self.exclude_boundaries:
            if transition.next_state is None:
                self.buffer = []
                return
        self.buffer = self.buffer[1:]

    def get(self, batch_size):
        """Samples the specified number of traces uniformly from the buffer."""
        traces = random.sample(self.traces, batch_size)
        return unpack(traces)

    def __len__(self):
        """Returns the number of traces stored."""
        return len(self.traces)


EPS = 0.001

class PrioritizedExperienceReplay:
    __doc__ = 'Stores prioritized interaction with an environment in a priority queue implemented via a heap.\n\n\tProvides efficient prioritized sampling of multistep traces.\n\tIf exclude_boundaries==True, then traces are sampled such that they don\'t include episode boundaries.\n\tFor more information see "Prioritized Experience Replay" (Schaul et al., 2016).\n\t'

    def __init__(self, capacity, steps=1, exclude_boundaries=False, prob_alpha=0.6):
        """
                Args:
                        capacity (int): The maximum number of traces the memory should be able to store.
                        steps (int): The number of steps (transitions) each sampled trace should include.
                        exclude_boundaries (bool): If True, sampled traces will not include episode boundaries.
                        prob_alpha (float): Value between 0 and 1 that specifies how strongly priorities are taken into account.
                """
        self.traces = []
        self.priorities = np.array([])
        self.buffer = []
        self.capacity = capacity
        self.steps = steps
        self.exclude_boundaries = exclude_boundaries
        self.prob_alpha = prob_alpha
        self.traces_idxs = []

    def put(self, transition):
        """Adds transition to memory."""
        self.buffer.append(transition)
        if len(self.buffer) < self.steps:
            return
        else:
            if len(self.traces) < self.capacity:
                self.traces.append(tuple(self.buffer))
                self.priorities = np.append(self.priorities, EPS if self.priorities.size == 0 else self.priorities.max())
            else:
                idx = np.argmin(self.priorities)
                self.traces[idx] = tuple(self.buffer)
                self.priorities[idx] = self.priorities.max()
        if self.exclude_boundaries:
            if transition.next_state is None:
                self.buffer = []
                return
        self.buffer = self.buffer[1:]

    def get(self, batch_size):
        """Samples the specified number of traces from the buffer according to the prioritization and prob_alpha."""
        probs = self.priorities ** self.prob_alpha
        probs /= probs.sum()
        self.traces_idxs = np.random.choice((len(self.traces)), batch_size, p=probs, replace=False)
        traces = [self.traces[idx] for idx in self.traces_idxs]
        return unpack(traces)

    def last_traces_idxs(self):
        """Returns the indexes associated with the last retrieved traces."""
        return self.traces_idxs.copy()

    def update_priorities(self, traces_idxs, new_priorities):
        """Updates the priorities of the traces with specified indexes."""
        self.priorities[traces_idxs] = new_priorities + EPS

    def __len__(self):
        """Returns the number of traces stored."""
        return len(self.traces)