# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/modeling/anchors/prior_box.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 2019 bytes
from itertools import product
import torch
from math import sqrt

class PriorBox:

    def __init__(self, cfg):
        self.image_size = cfg.INPUT.IMAGE_SIZE
        prior_config = cfg.MODEL.PRIORS
        self.feature_maps = prior_config.FEATURE_MAPS
        self.min_sizes = prior_config.MIN_SIZES
        self.max_sizes = prior_config.MAX_SIZES
        self.strides = prior_config.STRIDES
        self.aspect_ratios = prior_config.ASPECT_RATIOS
        self.clip = prior_config.CLIP

    def __call__(self):
        """Generate SSD Prior Boxes.
            It returns the center, height and width of the priors. The values are relative to the image size
            Returns:
                priors (num_priors, 4): The prior boxes represented as [[center_x, center_y, w, h]]. All the values
                    are relative to the image size.
        """
        priors = []
        for k, f in enumerate(self.feature_maps):
            scale = self.image_size / self.strides[k]
            for i, j in product((range(f)), repeat=2):
                cx = (j + 0.5) / scale
                cy = (i + 0.5) / scale
                size = self.min_sizes[k]
                h = w = size / self.image_size
                priors.append([cx, cy, w, h])
                size = sqrt(self.min_sizes[k] * self.max_sizes[k])
                h = w = size / self.image_size
                priors.append([cx, cy, w, h])
                size = self.min_sizes[k]
                h = w = size / self.image_size
                for ratio in self.aspect_ratios[k]:
                    ratio = sqrt(ratio)
                    priors.append([cx, cy, w * ratio, h / ratio])
                    priors.append([cx, cy, w / ratio, h * ratio])

        priors = torch.tensor(priors)
        if self.clip:
            priors.clamp_(max=1, min=0)
        return priors