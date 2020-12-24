# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/connectedThreshold.py
# Compiled at: 2018-09-14 08:53:17
# Size of source mod 2**32: 886 bytes
import SimpleITK as sitk, numpy as np, ctypes

def to_uint32(i):
    return ctypes.c_uint32(i).value


def connectedThreshold(img, seedCoordinates, lowerThreshold, upperThreshold):
    imgOriginal = img
    convertOutput = False
    if type(img) != sitk.SimpleITK.Image:
        imgOriginal = sitk.GetImageFromArray(img)
        convertOutput = True
    lstSeeds = [
     (
      to_uint32(int(seedCoordinates[1])), to_uint32(int(seedCoordinates[0])))]
    labelWhiteMatter = 1
    imgWhiteMatter = sitk.ConnectedThreshold(image1=imgOriginal, seedList=lstSeeds, lower=lowerThreshold, upper=upperThreshold, replaceValue=labelWhiteMatter)
    if convertOutput:
        imgWhiteMatter = sitk.GetArrayFromImage(imgWhiteMatter)
    return imgWhiteMatter