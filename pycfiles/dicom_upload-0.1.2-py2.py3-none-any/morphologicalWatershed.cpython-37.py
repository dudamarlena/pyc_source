# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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