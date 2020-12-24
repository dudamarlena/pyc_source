# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/data/causal_pair_generator.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5745 bytes
__doc__ = ' Pair Generator.\nGenerates pairs X,Y of variables with their labels.\nAuthor: Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from sklearn.preprocessing import scale
import numpy as np, pandas as pd
from .causal_mechanisms import LinearMechanism, Polynomial_Mechanism, SigmoidAM_Mechanism, SigmoidMix_Mechanism, GaussianProcessAdd_Mechanism, GaussianProcessMix_Mechanism, NN_Mechanism, gmm_cause, normal_noise
from joblib import delayed, Parallel
from ..utils.Settings import SETTINGS

class CausalPairGenerator(object):
    """CausalPairGenerator"""

    def __init__(self, causal_mechanism, noise=normal_noise, noise_coeff=0.4, initial_variable_generator=gmm_cause):
        super(CausalPairGenerator, self).__init__()
        self.mechanism = {'linear':LinearMechanism,  'polynomial':Polynomial_Mechanism, 
         'sigmoid_add':SigmoidAM_Mechanism, 
         'sigmoid_mix':SigmoidMix_Mechanism, 
         'gp_add':GaussianProcessAdd_Mechanism, 
         'gp_mix':GaussianProcessMix_Mechanism, 
         'nn':NN_Mechanism}[causal_mechanism]
        self.noise = noise
        self.noise_coeff = noise_coeff
        self.initial_generator = initial_variable_generator

    def generate(self, npairs, npoints=500, rescale=True, njobs=None):
        """Generate Causal pairs, such that one variable causes the other.

        Args:
            npairs (int): Number of pairs of variables to generate.
            npoints (int): Number of data points to generate.
            rescale (bool): Rescale the output with zero mean and unit variance.
            njobs (int): Number of parallel jobs to execute. Defaults to
                cdt.SETTINGS.NJOBS

        Returns:
            tuple: (pandas.DataFrame, pandas.DataFrame) data and corresponding
            labels. The data is at the ``SampleID, a (numpy.ndarray) , b (numpy.ndarray))``
            format.
        """

        def generate_pair(npoints, label, rescale):
            root = self.initial_generator(npoints)[:, np.newaxis]
            cause = self.mechanism(1, npoints, (self.noise), noise_coeff=(self.noise_coeff))(root)
            effect = self.mechanism(1, npoints, (self.noise), noise_coeff=(self.noise_coeff))(cause).squeeze(1)
            cause = cause.squeeze(1)
            if rescale:
                cause = scale(cause)
                effect = scale(effect)
            if label == 1:
                return (cause, effect)
            else:
                return (effect, cause)

        njobs = SETTINGS.get_default(njobs=njobs)
        self.labels = (np.random.randint(2, size=npairs) - 0.5) * 2
        output = [generate_pair(npoints, self.labels[i], rescale) for i in range(npairs)]
        self.data = pd.DataFrame(output, columns=['A', 'B'])
        self.labels = pd.DataFrame((self.labels), dtype='int32', columns=['label'])
        return (
         self.data, self.labels)

    def to_csv(self, fname_radical, **kwargs):
        """
        Save data to the csv format by default, in two separate files.

        Optional keyword arguments can be passed to pandas.
        """
        if self.data is not None:
            (self.data.to_csv)(fname_radical + '_data.csv', index=False, **kwargs)
            (self.labels.to_csv)(fname_radical + '_labels.csv', index=False, **kwargs)
        else:
            raise ValueError('Data has not yet been generated.                               Use self.generate() to do so.')