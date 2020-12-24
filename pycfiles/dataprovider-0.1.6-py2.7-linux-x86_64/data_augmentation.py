# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/data_augmentation.py
# Compiled at: 2016-11-29 20:56:28
"""

DataAugmentor

Kisuk Lee <kisuklee@mit.edu>, 2016
"""
from collections import OrderedDict
import numpy as np
from transform import *
aug_pool = [
 'warp', 'flip', 'grey', 'misalign']

class DataAugmentor(object):
    """
    Data augmentation.

    Attributes:
        _aug_list: List of data augmentation. Will be executed sequentially.
    """

    def __init__(self, spec):
        """
        TODO(kisuk): Documentation.
        """
        aug_list = []
        for s in spec:
            t = s['type']
            del s['type']
            t = t.lower()
            if t not in aug_pool:
                raise RuntimeError('unknown data augmentation type [%s]' % t)
            t = t[0].capitalize() + t[1:] + 'Augment'
            aug = eval(t + '(**s)')
            aug_list.append(aug)

        self._aug_list = aug_list

    def next_sample(self, dataset):
        raise NotImplementedError

    def random_sample(self, dataset):
        """
        TODO(kisuk): Documentation.
        """
        while True:
            try:
                spec = self._prepare(dataset)
                sample, transform = dataset.random_sample(spec=spec)
                break
            except:
                pass

        for aug in self._aug_list:
            sample = aug.augment(sample, imgs=dataset.get_imgs())

        sample = OrderedDict(sorted(sample.items(), key=lambda x: x[0]))
        return (sample, transform)

    def _prepare(self, dataset):
        ret = dict(dataset.get_spec())
        for aug in reversed(self._aug_list):
            ret = aug.prepare(ret, imgs=dataset.get_imgs(), **dataset.params)

        return ret


class DataAugment(object):
    """
    DataAugment interface.
    """

    def prepare(self, spec, **kwargs):
        raise NotImplementedError

    def augment(self, sample, **kwargs):
        raise NotImplementedError


class FlipAugment(DataAugment):
    """
    Random flip.
    """

    def prepare(self, spec, **kwargs):
        return dict(spec)

    def augment(self, sample, **kwargs):
        rule = np.random.rand(4) > 0.5
        return sample_func.flip(sample, rule=rule)


class GreyAugment(DataAugment):
    """
    Greyscale value augmentation.
    Randomly adjust contrast and brightness, and apply random gamma correction.
    """

    def __init__(self, mode='3D', skip_ratio=0.3):
        """
        Initialize parameters.

        Args:
            mode:
            ratio:
        """
        self.mode = mode
        self.ratio = skip_ratio
        assert mode == '3D' or mode == '2D' or mode == 'mix'
        self.CONTRAST_FACTOR = 0.3
        self.BRIGHTNESS_FACTOR = 0.3

    def prepare(self, spec, **kwargs):
        return dict(spec)

    def augment(self, sample, **kwargs):
        ret = sample
        if np.random.rand() > self.ratio:
            if self.mode == 'mix':
                mode = '3D' if np.random.rand() > 0.5 else '2D'
            else:
                mode = self.mode
            ret = eval(('self.augment{}(sample, **kwargs)').format(mode))
        return ret

    def augment2D(self, sample, **kwargs):
        """
        Adapted from ELEKTRONN (http://elektronn.org/).
        """
        imgs = kwargs['imgs']
        n = len(imgs)
        for i in range(n):
            key = imgs[i]
            for z in xrange(sample[key].shape[(-3)]):
                img = sample[key][..., z, :, :]
                img *= 1 + (np.random.rand() - 0.5) * self.CONTRAST_FACTOR
                img += (np.random.rand() - 0.5) * self.BRIGHTNESS_FACTOR
                img = np.clip(img, 0, 1)
                img **= 2.0 ** (np.random.rand() * 2 - 1)
                sample[key][..., z, :, :] = img

        return sample

    def augment3D(self, sample, **kwargs):
        """
        Adapted from ELEKTRONN (http://elektronn.org/).
        """
        imgs = kwargs['imgs']
        n = len(imgs)
        for i in range(n):
            key = imgs[i]
            sample[key] *= 1 + (np.random.rand() - 0.5) * self.CONTRAST_FACTOR
            sample[key] += (np.random.rand() - 0.5) * self.BRIGHTNESS_FACTOR
            sample[key] = np.clip(sample[key], 0, 1)
            sample[key] **= 2.0 ** (np.random.rand() * 2 - 1)

        return sample


class WarpAugment(DataAugment):
    """
    Warping.
    """

    def prepare(self, spec, **kwargs):
        pass

    def augment(self, sample, **kwargs):
        pass


from misalign import MisalignAugment
from warp import WarpAugment