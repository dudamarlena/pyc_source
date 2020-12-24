# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/newNameFromMetadata.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 827 bytes
from __future__ import print_function
import os
try:
    import dicom
except ImportError:
    import pydicom as dicom

def newNameFromMetadata(in_dir, verbose=False):
    filenames = os.listdir(in_dir)
    if verbose:
        print('newNameFromMetadata: input directory', in_dir)
        print('newNameFromMetadata: files in the direcotry', filenames)
    filename = filenames[0]
    dataset = dicom.read_file(in_dir + '/' + filename)
    oldname = dataset.PatientsName.split('^')
    if len(oldname) < 2:
        oldname = dataset.PatientsName.replace(',', '')
        oldname = oldname.split()
    print('WARNING:', dataset.PatientsName)
    new_person_name = oldname[0][0] + oldname[0][1] + oldname[1][0] + oldname[1][1]
    return new_person_name