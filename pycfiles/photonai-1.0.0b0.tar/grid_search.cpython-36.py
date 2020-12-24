# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/grid_search/grid_search.py
# Compiled at: 2019-09-11 10:06:07
# Size of source mod 2**32: 2910 bytes
import datetime, numpy as np
from photonai.optimization.base_optimizer import PhotonBaseOptimizer
from photonai.optimization.config_grid import create_global_config_grid
from photonai.photonlogger import Logger

class GridSearchOptimizer(PhotonBaseOptimizer):
    __doc__ = '\n    Searches for the best configuration by iteratively testing all possible hyperparameter combinations.\n    '

    def __init__(self):
        self.param_grid = []
        self.pipeline_elements = None
        self.parameter_iterable = None
        self.ask = self.next_config_generator()

    def prepare(self, pipeline_elements, maximize_metric):
        self.pipeline_elements = pipeline_elements
        self.ask = self.next_config_generator()
        self.param_grid = create_global_config_grid(self.pipeline_elements)
        Logger().info('Grid Search generated ' + str(len(self.param_grid)) + ' configurations')

    def next_config_generator(self):
        for parameters in self.param_grid:
            yield parameters

    def tell(self, config, performance):
        pass


class RandomGridSearchOptimizer(GridSearchOptimizer):
    __doc__ = '\n     Searches for the best configuration by randomly testing k possible hyperparameter combinations.\n    '

    def __init__(self, k=None):
        super(RandomGridSearchOptimizer, self).__init__()
        self.k = k

    def prepare(self, pipeline_elements, maximize_metric):
        super(RandomGridSearchOptimizer, self).prepare(pipeline_elements, maximize_metric)
        self.param_grid = list(self.param_grid)
        np.random.shuffle(self.param_grid)
        if self.k is not None:
            if self.k > len(self.param_grid):
                self.k = len(self.param_grid)
            self.param_grid = self.param_grid[0:self.k]


class TimeBoxedRandomGridSearchOptimizer(RandomGridSearchOptimizer):
    __doc__ = '\n    Iteratively tests k possible hyperparameter configurations until a certain time limit is reached.\n    '

    def __init__(self, limit_in_minutes=60):
        super(TimeBoxedRandomGridSearchOptimizer, self).__init__()
        self.limit_in_minutes = limit_in_minutes
        self.start_time = None
        self.end_time = None

    def prepare(self, pipeline_elements, maximize_metric):
        super(TimeBoxedRandomGridSearchOptimizer, self).prepare(pipeline_elements, maximize_metric)
        self.start_time = None

    def next_config_generator(self):
        if self.start_time is None:
            self.start_time = datetime.datetime.now()
            self.end_time = self.start_time + datetime.timedelta(minutes=(self.limit_in_minutes))
        for parameters in super(TimeBoxedRandomGridSearchOptimizer, self).next_config_generator():
            if datetime.datetime.now() < self.end_time:
                yield parameters