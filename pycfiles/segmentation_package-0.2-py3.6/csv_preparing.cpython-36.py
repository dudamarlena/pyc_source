# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\segmentation_module\segmentation_support\csv_preparing.py
# Compiled at: 2019-04-15 06:09:30
# Size of source mod 2**32: 1547 bytes
import glob, os, re, numpy as np, pandas as pd
from segmentation_module.segmentation_tools.utils2 import get_photos_from_dir

def get_images_paths(images_path, dataset):
    filenames = get_photos_from_dir(os.path.join(images_path, dataset))
    return filenames


images_path = 'D:\\segmentation_labels_15_04_2019\\images'
labels_path = 'D:\\segmentation_labels_15_04_2019\\labels'
images_path = os.path.normpath(images_path)
labels_path = os.path.normpath(labels_path)
datasets = [
 'train', 'val', 'test']
for dataset in datasets:
    filenames_im = get_images_paths(images_path, dataset)
    filenames_im = [os.path.join(dataset, os.path.basename(x)) for x in filenames_im]
    filenames_lb = get_images_paths(labels_path, dataset)
    filenames_lb = [os.path.join(dataset, os.path.basename(x)) for x in filenames_lb]
    concat = np.vstack([filenames_im, filenames_lb]).transpose()
    df = pd.DataFrame(concat, columns=['images', 'labels'])
    df.to_csv((dataset + '.csv'), index=False)