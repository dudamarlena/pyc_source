# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/projects_nils/photon_core/photonai/optimization/random_search/random_search.py
# Compiled at: 2019-11-21 09:20:09
# Size of source mod 2**32: 2439 bytes
import datetime, random
from photonai.optimization.base_optimizer import PhotonBaseOptimizer
import photonai.photonlogger.logger as logger

class RandomSearchOptimizer(PhotonBaseOptimizer):
    __doc__ = '\n     Searches for the best configuration by randomly testing k possible hyperparameter combinations without grid.\n    '

    def __init__(self, n_configurations=None, limit_in_minutes=60):
        self.pipeline_elements = None
        self.parameter_iterable = None
        self.ask = self.next_config_generator()
        self.n_configurations = None
        if not limit_in_minutes or limit_in_minutes <= 0:
            self.limit_in_minutes = None
        else:
            self.limit_in_minutes = limit_in_minutes
        self.start_time = None
        self.end_time = None
        if not n_configurations or n_configurations <= 0:
            self.n_configurations = None
        else:
            self.n_configurations = n_configurations
        self.k_configutration = 0
        if not n_configurations:
            if limit_in_minutes <= 0:
                msg = 'No stopping criteria for RandomSearchOptimizer.'
                logger.warn(msg)

    def prepare(self, pipeline_elements, maximize_metric):
        self.pipeline_elements = pipeline_elements
        self.ask = self.next_config_generator()

    def next_config_generator(self):
        while 1:
            val = yield self.generate_config()
            self.k_configutration += 1
            if self.limit_in_minutes:
                if self.start_time is None:
                    self.start_time = datetime.datetime.now()
                    self.end_time = self.start_time + datetime.timedelta(minutes=(self.limit_in_minutes))
                if datetime.datetime.now() >= self.end_time:
                    return
            if self.n_configurations and self.k_configutration >= self.n_configurations:
                return

    def tell(self, config, performance):
        pass

    def generate_config(self):
        config = {}
        for p_element in self.pipeline_elements:
            for h_key, h_value in p_element.hyperparameters.items():
                if isinstance(h_value, list):
                    config[h_key] = random.choice(h_value)
                else:
                    config[h_key] = h_value.get_random_value()

        return config