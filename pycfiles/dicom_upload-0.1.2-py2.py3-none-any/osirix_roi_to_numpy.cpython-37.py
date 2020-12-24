# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/osirix_roi_to_numpy.py
# Compiled at: 2018-06-23 13:19:25
# Size of source mod 2**32: 1493 bytes
__doc__ = '\nImport an Osirix xml roi as a binary numpy array\n\nRequires libraries:\nnibabel\nnumpy\nscikit-image\nxml\n\nBenjamin Irving\n2014/03/31\n\nLicence:\nBSD\n\n'
from __future__ import print_function, division
import xml.etree.ElementTree as ET
from skimage.draw import polygon
import numpy as np

def osirix_roi_to_numpy(imshape, file_xml):
    """
    This function loads a osirix xml region as a binary numpy array

    @imshape : The shape of the 3D volume as an array e.g. [512 512 40]
    @file_xml : xml file of the annotation
    
    return: numpy array where positions in the roi are assigned a value of 1. 
    
    """
    tree = ET.parse(file_xml)
    root = tree.getroot()
    data1 = root[0][1]
    roi1 = np.zeros(imshape)
    for ii in data1:
        slice1 = int(ii.find('integer').text) - 1
        print('Slice ', slice1)
        pp = ii.findall('array')
        x = []
        y = []
        for jj in pp[1]:
            coord_text = jj.text
            coord1 = coord_text.strip('{},').split(',')
            x.append(float(coord1[0]))
            y.append(imshape[1] - float(coord1[1]))

        y1 = np.array(y)
        x1 = np.array(x)
        rr, cc = polygon(x1, y1)
        roi1[(rr, cc, slice1)] = 1

    return roi1