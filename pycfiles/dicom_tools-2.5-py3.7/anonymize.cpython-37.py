# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/anonymize.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5068 bytes
"""Read a dicom file (or directory of files), partially "anonymize" it (them),
by replacing Person names, patient id, optionally remove curves
and private tags, and write result to a new file (directory)
This is an example only; use only as a starting point.
"""
from __future__ import print_function
usage = '\nUsage:\npython anonymize.py dicomfile.dcm outputfile.dcm\nOR\npython anonymize.py originals_directory anonymized_directory\n\nNote: Use at your own risk. Does not fully de-identify the DICOM data as per\nthe DICOM standard, e.g in Annex E of PS3.15-2011.\n'
import os, os.path
try:
    import dicom
    from dicom.errors import InvalidDicomError
except ImportError:
    import pydicom as dicom
    from pydicom.errors import InvalidDicomError

def anonymizefile(filename, output_filename, new_person_name='AUTO', new_patient_id='id', remove_curves=True, remove_private_tags=True):
    """Replace data element values to partly anonymize a DICOM file.
    Note: completely anonymizing a DICOM file is very complicated; there
    are many things this example code does not address. USE AT YOUR OWN RISK.
    """

    def PN_callback(ds, data_element):
        if data_element.VR == 'PN':
            data_element.value = new_person_name

    def curves_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.tag.group & 65280 == 20480:
            del ds[data_element.tag]

    dataset = dicom.read_file(filename)
    oldname = dataset.PatientsName.split('^')
    if new_person_name == 'AUTO':
        new_person_name = oldname[0][0] + oldname[0][1] + oldname[1][0] + oldname[1][1]
    print('new person name:', new_person_name)
    dataset.walk(PN_callback)
    dataset.PatientID = new_patient_id
    for name in ('OtherPatientIDs', 'OtherPatientIDsSequence'):
        if name in dataset:
            delattr(dataset, name)

    for name in ('PatientBirthDate', ):
        if name in dataset:
            dataset.data_element(name).value = ''

    if remove_private_tags:
        dataset.remove_private_tags()
    if remove_curves:
        dataset.walk(curves_callback)
    dataset.save_as(output_filename)


def anonymize(inp, out, new_person_name='AUTO', verbose=False):
    if os.path.isdir(inp):
        in_dir = inp
        out_dir = out
        if os.path.exists(out_dir) and not os.path.isdir(out_dir):
            raise IOError('Input is directory; output name exists but is not a directory')
        else:
            os.makedirs(out_dir)
        filenames = os.listdir(in_dir)
        for filename in filenames:
            if filename == 'DICOMDIR':
                continue
            if not os.path.isdir(os.path.join(in_dir, filename)):
                print((filename + '...'), end='')
                try:
                    if verbose:
                        print('anonymize', os.path.join(in_dir, filename), os.path.join(out_dir, filename), new_person_name)
                    anonymizefile(os.path.join(in_dir, filename), os.path.join(out_dir, filename), new_person_name)
                except InvalidDicomError:
                    print('Not a valid dicom file, may need force=True on read_file\r')
                else:
                    print('done\r')

    else:
        in_filename = inp
        out_filename = out
        anonymizefile(in_filename, out_filename, new_person_name)
    print()