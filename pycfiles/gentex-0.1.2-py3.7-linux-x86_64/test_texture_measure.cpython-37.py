# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_texture_measure.py
# Compiled at: 2019-10-04 13:17:54
# Size of source mod 2**32: 3707 bytes
import gentex, numpy as np, imageio
from PIL import Image
from pathlib import Path
FIXTURE_DIR = Path(__file__).parents[0] / 'fixtures'

def test_texture_measure():
    texm = [
     'CM Entropy',
     'EM Entropy',
     'Statistical Complexity',
     'Energy Uniformity',
     'Maximum Probability',
     'Contrast',
     'Inverse Difference Moment',
     'Correlation',
     'Probability of Run Length',
     'Epsilon Machine Run Length',
     'Run Length Asymmetry',
     'Homogeneity',
     'Cluster Tendency',
     'Multifractal Spectrum Energy Range',
     'Multifractal Spectrum Entropy Range']
    im = imageio.imread(FIXTURE_DIR / 'test_image.png')
    mask = np.where(im > 0, 1, 0)
    box_indices = gentex.template.Template('RectBox', [7, 7, 7], 2, False).offsets
    levels = 4
    fe = gentex.features.Features([im], mask, box_indices)
    fe.clusfs(numclus=levels)
    comat = gentex.comat.comat_mult((fe.clusim), mask, box_indices, levels=levels)
    mytex = gentex.texmeas.Texmeas(comat)
    mytex.coordmom = 2
    mytex.probmom = 2
    mytex.clusmom = 2
    mytex.rllen = 0.1
    for meas in texm:
        mytex.calc_measure(meas)
        print('\t', meas, '= ', mytex.val)


def test_texture_measure_voxel_wise():
    texm = [
     'CM Entropy']
    im = Image.open(FIXTURE_DIR / 'test_image.png')
    im = np.asarray(im.resize(tuple(map(lambda x: x // 4, im.size))))
    mask2 = np.where(im > 0, 1, 0)
    idx, idy = np.where(mask2 == 1)
    mask1 = np.zeros((im.shape), dtype=int)
    res = np.zeros(im.shape + (len(texm),))
    box_indices = gentex.template.Template('RectBox', [7, 7, 7], 2, False).offsets
    levels = 8
    bins = np.linspace(im.min(), im.max(), levels + 1)
    im_q = np.digitize(im.ravel(), bins).reshape(im.shape) - 1
    for a, b in zip(idx, idy):
        mask1[(a, b)] = 1
        comat = gentex.comat.comat_2T_mult(im_q, mask1, im_q, mask2, box_indices, levels1=(levels + 1),
          levels2=(levels + 1))
        mytex = gentex.texmeas.Texmeas(comat)
        for c, meas in enumerate(texm):
            mytex.calc_measure(meas)
            res[(a, b, c)] = mytex.val

        mask1[(a, b)] = 0