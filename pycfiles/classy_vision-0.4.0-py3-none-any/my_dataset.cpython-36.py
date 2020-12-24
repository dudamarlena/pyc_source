# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mannatsingh/dev/git/upstream/ClassyVision/classy_vision/templates/synthetic/datasets/my_dataset.py
# Compiled at: 2020-04-29 11:26:04
# Size of source mod 2**32: 1788 bytes
from typing import Any, Callable, Dict, Optional, Union
from classy_vision.dataset import ClassyDataset, register_dataset
from classy_vision.dataset.core.random_image_datasets import RandomImageBinaryClassDataset, SampleType
from classy_vision.dataset.transforms import ClassyTransform, build_transforms

@register_dataset('my_dataset')
class MyDataset(ClassyDataset):

    def __init__(self, batchsize_per_replica, shuffle, transform, num_samples, crop_size, class_ratio, seed):
        dataset = RandomImageBinaryClassDataset(crop_size, class_ratio, num_samples, seed, SampleType.TUPLE)
        super().__init__(dataset, batchsize_per_replica, shuffle, transform, num_samples)

    @classmethod
    def from_config(cls, config: Dict[(str, Any)]) -> 'MyDataset':
        assert all(key in config for key in ('crop_size', 'class_ratio', 'seed'))
        crop_size = config['crop_size']
        class_ratio = config['class_ratio']
        seed = config['seed']
        transform_config, batchsize_per_replica, shuffle, num_samples = cls.parse_config(config)
        transform = build_transforms(transform_config)
        return cls(batchsize_per_replica, shuffle, transform, num_samples, crop_size, class_ratio, seed)