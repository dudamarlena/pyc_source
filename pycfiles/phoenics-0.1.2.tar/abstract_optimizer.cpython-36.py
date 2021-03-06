# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/flo/Phoenics/master/src/phoenics/Acquisition/NumpyOptimizers/abstract_optimizer.py
# Compiled at: 2019-11-24 12:43:13
# Size of source mod 2**32: 1886 bytes
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
import numpy as np

class AbstractOptimizer(object):
    dx = 1e-06

    def __init__(self, func, *args, **kwargs):
        self.func = func
        for key, value in kwargs.items():
            setattr(self, str(key), value)

    def _set_func(self, func, pos=None):
        self.func = func
        if pos is not None:
            self.pos = pos
            self.num_pos = len(pos)

    def grad(self, sample, step=None):
        if step is None:
            step = self.dx
        gradients = np.zeros((len(sample)), dtype=(np.float32))
        perturb = np.zeros((len(sample)), dtype=(np.float32))
        for pos_index, pos in enumerate(self.pos):
            if pos is None:
                pass
            else:
                perturb[pos] += step
                gradient = (self.func(sample + perturb) - self.func(sample - perturb)) / (2.0 * step)
                gradients[pos] = gradient
                perturb[pos] -= step

        return gradients