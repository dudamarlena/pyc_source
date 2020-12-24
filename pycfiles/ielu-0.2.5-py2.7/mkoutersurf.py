# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ielu/mkoutersurf.py
# Compiled at: 2016-03-02 14:09:44
import sys, numpy as np, nibabel as nib
from scipy.signal import convolve
from scipy.ndimage.morphology import grey_closing
from scipy.ndimage.morphology import generate_binary_structure
from mne import write_surface
from mcubes import marching_cubes

def mkoutersurf(image, radius, outfile):
    fill = nib.load(image)
    filld = fill.get_data()
    filld[filld == 1] = 255
    gaussian = np.ones((2, 2)) * 0.25
    image_f = np.zeros((256, 256, 256))
    for slice in xrange(256):
        temp = filld[:, :, slice]
        image_f[:, :, slice] = convolve(temp, gaussian, 'same')

    image2 = np.zeros((256, 256, 256))
    image2[np.where(image_f <= 25)] = 0
    image2[np.where(image_f > 25)] = 255
    strel15 = generate_binary_structure(3, 1)
    BW2 = grey_closing(image2, structure=strel15)
    thresh = np.max(BW2) / 2
    BW2[np.where(BW2 <= thresh)] = 0
    BW2[np.where(BW2 > thresh)] = 255
    v, f = marching_cubes(BW2, 100)
    v2 = np.transpose(np.vstack((128 - v[:, 0],
     v[:, 2] - 128,
     128 - v[:, 1])))
    write_surface(outfile, v2, f)


if __name__ == '__main__':
    if not len(sys.argv) == 4:
        raise ValueError('the fail at give argument correct,\nvolume filled first, diameter integral then, arguments file output')
    mkoutersurf(sys.argv[1], None, sys.argv[3])