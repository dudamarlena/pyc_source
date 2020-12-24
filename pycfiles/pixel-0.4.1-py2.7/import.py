# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pixel/import.py
# Compiled at: 2016-09-28 10:30:55
from tqdm import tqdm
import numpy as np, deepzoom
creator = deepzoom.ImageCreator(tile_format='png', image_quality=1.0, resize_filter='nearest', tile_size=1024, tile_overlap=1)
import h5py, scipy.misc, StringIO
with h5py.File('/usr/people/it2/seungmount/research/datasets/blended_piriform_157x2128x2128/all/image.h5') as (f):
    channel = f['/main'][:]
with h5py.File('/usr/people/it2/seungmount/research/datasets/blended_piriform_157x2128x2128/all/human_labels.h5') as (f):
    segmentation = f['/main'][:]
img = segmentation + channel * 2 ** 24
for z in tqdm(xrange(img.shape[0])):
    creator.create(img[z, :, :], ('./piriform/{}.dzi').format(z))