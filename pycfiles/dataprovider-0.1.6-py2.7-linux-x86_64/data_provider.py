# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/data_provider.py
# Compiled at: 2016-11-29 20:56:28
"""

DaraProvider classes.

Kisuk Lee <kisuklee@mit.edu>, 2015-2016
"""
from collections import OrderedDict
import numpy as np, parser
from dataset import VolumeDataset
from data_augmentation import DataAugmentor
from transform import *
from label_transform import *

class DataProvider(object):
    """
    DataProvider interface.
    """

    def next_sample(self):
        raise NotImplementedError

    def random_sample(self):
        raise NotImplementedError


class VolumeDataProvider(DataProvider):
    """
    DataProvider for volumetric data.

    Attributes:
        datasets: List of datasets.
        _sampling_weights: Probability of each dataset being chosen at each
                            iteration.
        _net_spec: Dictionary mapping layers' name to their input dimension.
    """

    def __init__(self, dspec_path, net_spec, params, auto_mask=True):
        """
        Initialize DataProvider.

        Args:
            dspec_path: Path to the dataset specification file.
            net_spec:   Net specification.
            params:     Various options.
            auto_mask:  Whether to automatically generate mask from
                        corresponding label.
        """
        drange = params['drange']
        dprior = params.get('dprior', None)
        print '\n[VolumeDataProvider]'
        p = parser.Parser(dspec_path, net_spec, params, auto_mask=auto_mask)
        self.datasets = list()
        for d in drange:
            print 'constructing dataset %d...' % d
            config, dparams = p.parse_dataset(d)
            dataset = VolumeDataset(config, **dparams)
            self.datasets.append(dataset)

        self.set_sampling_weights(dprior)
        aug_spec = params.get('augment', [])
        self._data_aug = DataAugmentor(aug_spec)
        return

    def set_sampling_weights(self, dprior=None):
        """
        TODO(kisuk): Documentation.
        """
        if dprior is None:
            dprior = [ x.num_sample() for x in self.datasets ]
        dprior = np.asarray(dprior, dtype='float32')
        dprior = dprior / np.sum(dprior)
        self._sampling_weights = dprior
        return

    def next_sample(self):
        """Fetch next sample in a sample sequence."""
        return self.random_sample()

    def random_sample(self):
        """Fetch random sample."""
        dataset = self._get_random_dataset()
        sample, transform = self._data_aug.random_sample(dataset)
        sample = self._transform(sample, transform)
        return OrderedDict(sorted(sample.items(), key=lambda x: x[0]))

    def _get_random_dataset(self):
        """
        Pick one dataset randomly, according to the given sampling weights.

        Returns:
            Randomly chosen dataset.
        """
        if len(self.datasets) == 1:
            return self.datasets[0]
        sq = np.random.multinomial(1, self._sampling_weights, size=1)
        sq = np.squeeze(sq)
        idx = np.nonzero(sq)[0][0]
        return self.datasets[idx]

    def _transform(self, sample, transform):
        """
        TODO(kisuk): Documentation.
        """
        affinitized = False
        for key, spec in transform.iteritems():
            if spec is not None:
                if spec['type'] == 'affinitize':
                    affinitized = True
                label_func.evaluate(sample, key, spec)

        if affinitized:
            for key, data in sample.iteritems():
                sample[key] = tensor_func.crop(data, (1, 1, 1))

        return sample