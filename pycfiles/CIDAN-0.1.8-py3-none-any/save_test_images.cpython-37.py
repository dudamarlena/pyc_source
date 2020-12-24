# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/LSSC/functions/save_test_images.py
# Compiled at: 2020-04-05 17:28:46
# Size of source mod 2**32: 2583 bytes
from CIDAN.LSSC.functions import data_manipulation
import numpy as np, os
import matplotlib.pyplot as plt

def save_volume_images(volume, output_dir):
    data_manipulation.save_image(volume, 'original_image_filtered',
      output_dir,
      (volume.shape),
      number_save=4)
    data_manipulation.save_image(np.max(volume, axis=0), 'max_intensity_filtered',
      output_dir,
      (
     1, volume.shape[1],
     volume.shape[2]),
      number_save=1)
    data_manipulation.save_image(np.mean(volume, axis=0), 'mean_intensity_filtered',
      output_dir,
      (
     1, volume.shape[1],
     volume.shape[2]),
      number_save=1)


def save_eigen_images(eigen_vectors, output_dir, image_shape, box_num=0):
    e_vectors_squared = np.power(eigen_vectors, 2)
    e_vectors_reshape = np.transpose(np.reshape(e_vectors_squared, (
     image_shape[1],
     image_shape[2], eigen_vectors.shape[1]),
      order='C'), (2, 0, 1))
    data_manipulation.save_image(e_vectors_reshape, ('box_{}_eigen_vectors'.format(str(box_num).zfill(2))),
      output_dir,
      (e_vectors_reshape.shape),
      number_save=(eigen_vectors.shape[1]))


def save_roi_images(roi_list, image_shape, output_dir, box_num=0):
    pixel_length = image_shape[1] * image_shape[2]
    original_zeros_all = np.zeros(pixel_length)
    for num, x in enumerate(roi_list):
        original_zeros = np.zeros(pixel_length)
        original_zeros_all[x] = 255
        original_zeros[x] = 255
        imgplot = plt.imshow(np.reshape(original_zeros, (
         image_shape[1],
         image_shape[2])))
        plt.savefig(os.path.join(output_dir, 'box_{}_roi_{}'.format(str(box_num).zfill(2), str(num).zfill(3)) + '_' + str(0)))

    data_manipulation.save_image(original_zeros_all, 'box_{}_roi_all'.format(str(box_num).zfill(2)), output_dir, (
     1, image_shape[1],
     image_shape[2]), 1)