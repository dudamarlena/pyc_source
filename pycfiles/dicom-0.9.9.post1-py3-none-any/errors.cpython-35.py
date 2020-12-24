# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\errors.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 904 bytes
"""Module for pydicom exception classes"""

class InvalidDicomError(Exception):
    __doc__ = 'Exception that is raised when the the file does not seem\n    to be a valid dicom file, usually when the four characters\n    "DICM" are not present at position 128 in the file.\n    (According to the dicom specification, each dicom file should\n    have this.)\n\n    To force reading the file (because maybe it is a dicom file without\n    a header), use read_file(..., force=True).\n    '

    def __init__(self, *args):
        if not args:
            args = ('The specified file is not a valid DICOM file.', )
        Exception.__init__(self, *args)