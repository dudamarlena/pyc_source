# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/sitk_show.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 601 bytes
import numpy, SimpleITK
import matplotlib.pyplot as plt

def sitk_show(img, title=None, margin=0.05, dpi=40):
    nda = SimpleITK.GetArrayFromImage(img)
    spacing = img.GetSpacing()
    figsize = ((1 + margin) * nda.shape[0] / dpi, (1 + margin) * nda.shape[1] / dpi)
    extent = (0, nda.shape[1] * spacing[1], nda.shape[0] * spacing[0], 0)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
    plt.set_cmap('gray')
    ax.imshow(nda, extent=extent, interpolation=None)
    if title:
        plt.title(title)
    plt.show()