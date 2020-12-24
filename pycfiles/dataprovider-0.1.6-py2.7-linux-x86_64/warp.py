# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/warp.py
# Compiled at: 2016-11-29 20:56:28
"""

Warp data augmentation.

Kisuk Lee <kisuklee@mit.edu>, 2016
"""
from box import Box
import data_augmentation
from warping import _warping
import numpy as np
from utils import check_tensor, check_volume
from vector import Vec3d

class WarpAugment(data_augmentation.DataAugment):
    """
    Warp.
        1. Continuous rotation
        2. Shear
        3. Twist
        4. Scale
        5. Perspective stretch
    """

    def __init__(self, skip_ratio=0.3):
        """Initialize WarpAugment."""
        self.ratio = skip_ratio

    def prepare(self, spec, **kwargs):
        """
        Randomly draw warp parameters and compute required (mostly
        larger than original) image sizes.
        """
        self.skip = False
        if self.ratio > np.random.rand():
            self.skip = True
            return dict(spec)
        imgs = kwargs['imgs']
        b = Box((0, 0, 0), (0, 0, 0))
        for k, v in spec.iteritems():
            b = b.merge(Box((0, 0, 0), v[-3:]))

        maxsz = tuple(b.size())
        params = warping.getWarpParams(maxsz, **kwargs)
        self.size = tuple(x for x in params[0])
        size_diff = tuple(x - y for x, y in zip(self.size, maxsz))
        self.rot = params[1]
        self.shear = params[2]
        self.scale = params[3]
        self.stretch = params[4]
        self.twist = params[5]
        self.spec = dict(spec)
        ret = dict()
        for k, v in spec.iteritems():
            if k in imgs:
                ret[k] = v[:-3] + self.size
            else:
                ret[k] = v[:-3] + tuple(x + y for x, y in zip(v[-3:], size_diff))

        return ret

    def augment(self, sample, **kwargs):
        """Apply warp data augmentation."""
        if self.skip:
            return sample
        imgs = kwargs['imgs']
        for k, v in sample.iteritems():
            v = check_tensor(v)
            v = np.transpose(v, (1, 0, 2, 3))
            if k in imgs:
                v = warping.warp3d(v, self.spec[k][-3:], self.rot, self.shear, self.scale, self.stretch, self.twist)
            else:
                v = warping.warp3dLab(v, self.spec[k][-3:], self.size, self.rot, self.shear, self.scale, self.stretch, self.twist)
            sample[k] = np.transpose(v, (1, 0, 2, 3))

        return sample


if __name__ == '__main__':
    spec = dict()
    spec['input/p3'] = (5, 109, 109)
    spec['input/p2'] = (7, 73, 73)
    spec['input/p1'] = (9, 45, 45)
    spec['label'] = (3, 1, 1, 1)
    outsz = Vec3d(5, 100, 100)
    for k, v in spec.iteritems():
        newv = tuple(Vec3d(v[-3:]) + outsz - Vec3d(1, 1, 1))
        spec[k] = v[:-3] + newv

    aug = WarpAugment()
    ret = aug.prepare(spec, imgs=['input/p3', 'input/p2', 'input/p1'])
    print ret
    print aug.spec
    print aug.rot
    print aug.shear
    print aug.scale
    print aug.stretch
    print aug.twist