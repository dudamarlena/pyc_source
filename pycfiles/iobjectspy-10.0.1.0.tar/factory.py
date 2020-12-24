# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\datasets\factory.py
# Compiled at: 2019-12-31 04:09:01
# Size of source mod 2**32: 1080 bytes
"""Factory method for easily getting imdbs by name."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
__sets = {}
import datasets.pascal_voc as pascal_voc
for split in ('train', 'val', 'trainval', 'test'):
    name = 'voc_{}'.format(split)
    __sets[name] = lambda split=split: pascal_voc(split)

for split in ('train', 'val', 'trainval', 'test'):
    name = 'voc_{}_diff'.format(split)
    __sets[name] = lambda split=split: pascal_voc(split, use_diff=True)

def get_imdb(name):
    """Get an imdb (image database) by name."""
    if name not in __sets:
        raise KeyError('Unknown dataset: {}'.format(name))
    return __sets[name]()


def list_imdbs():
    """List all registered imdbs."""
    return list(__sets.keys())