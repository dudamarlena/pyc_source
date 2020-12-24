# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/flo/Phoenics/master/src/phoenics/BayesianNetwork/bayesian_network.py
# Compiled at: 2019-11-24 14:38:42
# Size of source mod 2**32: 4914 bytes
"""
Licensed to the Apache Software Foundation (ASF) under one or more 
contributor license agreements. See the NOTICE file distributed with this 
work for additional information regarding copyright ownership. The ASF 
licenses this file to you under the Apache License, Version 2.0 (the 
"License"); you may not use this file except in compliance with the 
License. You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software 
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
License for the specific language governing permissions and limitations 
under the License.

The code in this file was developed at Harvard University (2018) and 
modified at ChemOS Inc. (2019) as stated in the NOTICE file.
"""
__author__ = 'Florian Hase'
import os, time, pickle, subprocess, numpy as np
from utilities import Logger
from utilities import PhoenicsUnknownSettingsError
from .kernel_evaluations import KernelEvaluator

class BayesianNetwork(Logger):

    def __init__(self, config, model_details=None):
        self.COUNTER = 0
        self.has_sampled = False
        self.config = config
        verbosity = self.config.get('verbosity')
        if 'bayesian_network' in verbosity:
            verbosity = verbosity['bayesian_network']
        else:
            Logger.__init__(self, 'BayesianNetwork', verbosity=verbosity)
            self.kernel_contribution = lambda x: (np.sum(x), 1.0)
            if model_details == None:
                from BayesianNetwork.model_details import model_details
            self.model_details = model_details
            if self.config.get('backend') == 'tfprob':
                from BayesianNetwork.TfprobInterface import TfprobNetwork
                self.network_executable = '{}/BayesianNetwork/TfprobInterface/tfprob_interface.py'.format(self.config.get('home'))
            else:
                if self.config.get('backend') == 'edward':
                    from BayesianNetwork.EdwardInterface import EdwardNetwork
                    self.network_executable = '%s/BayesianNetwork/EdwardInterface/edward_interface.py' % self.config.get('home')
                else:
                    PhoenicsUnknownSettingsError('did not understand backend: "%s".\n\tChoose from "tfprob" or "edward"' % self.config_general.backend)
            self.volume = 1.0
            feature_lengths = self.config.feature_lengths
            feature_ranges = self.config.feature_ranges
            for feature_index, feature_type in enumerate(self.config.feature_types):
                self.volume *= feature_ranges[feature_index]

            self.inverse_volume = 1 / self.volume
            if self.config.get('sampling_strategies') == 1:
                self.sampling_param_values = np.zeros(1)
            else:
                self.sampling_param_values = np.linspace(-1.0, 1.0, self.config.get('sampling_strategies'))
            self.sampling_param_values = self.sampling_param_values[::-1]
        self.sampling_param_values *= self.inverse_volume

    def sample(self, obs_params, obs_objs, num_epochs=None):
        sim_data = {'config':self.config, 
         'model_details':self.model_details,  'obs_params':obs_params,  'obs_objs':obs_objs}
        sim_file = '%s/sampling_information.pkl' % self.config.get('scratch_dir')
        with open(sim_file, 'wb') as (content):
            pickle.dump(sim_data, content)
        results_file = '%s/sampling_results.pkl' % self.config.get('scratch_dir')
        subprocess.call(('python %s %s %s %s' % (self.network_executable, self.config.get('home'), sim_file, results_file)), shell=True)
        with open(results_file, 'rb') as (content):
            results_dict = pickle.loads(content.read())
        self.trace_kernels = results_dict['trace_kernels']
        self.obs_objs = results_dict['obs_objs']
        self.has_sampled = True

    def build_kernels(self):
        if not self.has_sampled:
            raise AssertionError
        else:
            trace_kernels = self.trace_kernels
            obs_objs = self.obs_objs
            locs = trace_kernels['locs']
            sqrt_precs = trace_kernels['sqrt_precs']
            if self.config.get('boosted'):
                lower_prob_bound = 0.1
                for size in self.config.feature_ranges:
                    lower_prob_bound *= 1.0 / size

            else:
                lower_prob_bound = 1e-25
        self.kernel_evaluator = KernelEvaluator(locs, sqrt_precs, lower_prob_bound, obs_objs, self.inverse_volume)

        def kernel_contribution(proposed_sample):
            num, inv_den, _ = self.kernel_evaluator.get_kernel(proposed_sample.astype(np.float64))
            return (num, inv_den)

        self.kernel_contribution = kernel_contribution