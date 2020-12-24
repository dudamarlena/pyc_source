# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/curvatureFlowImageFilter.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 661 bytes
import numpy as np, SimpleITK as sitk

def curvatureFlowImageFilter(img, verbose=False):
    imgOriginal = img
    convertOutput = False
    if type(img) != sitk.SimpleITK.Image:
        imgOriginal = sitk.GetImageFromArray(img)
        convertOutput = True
    imgSmooth = sitk.CurvatureFlow(image1=imgOriginal, timeStep=0.125,
      numberOfIterations=5)
    if convertOutput:
        imgSmooth = sitk.GetArrayFromImage(imgSmooth).astype(float)
    return imgSmooth