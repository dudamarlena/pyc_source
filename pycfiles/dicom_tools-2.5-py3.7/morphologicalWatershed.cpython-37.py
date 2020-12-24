# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/morphologicalWatershed.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 669 bytes
import SimpleITK as sitk, numpy as np, ctypes

def to_uint32(i):
    return ctypes.c_uint32(i).value


def morphologicalWatershed(img, level=10, fullyConnected=False):
    imgOriginal = img
    convertOutput = False
    if type(img) != sitk.SimpleITK.Image:
        imgOriginal = sitk.GetImageFromArray(img)
        convertOutput = True
    feature_img = sitk.GradientMagnitude(imgOriginal)
    ws_img = sitk.MorphologicalWatershed(feature_img, level=level, markWatershedLine=True, fullyConnected=fullyConnected)
    ws_img = sitk.LabelToRGB(ws_img)
    if convertOutput:
        ws_img = sitk.GetArrayFromImage(ws_img).astype(float)
    return ws_img