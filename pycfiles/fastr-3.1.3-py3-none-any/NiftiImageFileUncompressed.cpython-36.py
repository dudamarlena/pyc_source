# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/NiftiImageFileUncompressed.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 1932 bytes
import os
from fastr.datatypes import URLType

class NiftiImageFileUncompressed(URLType):
    description = 'Nifti Image File format'
    extension = 'nii'

    def _validate(self):
        parsed_value = self.parsed_value
        if self.extension:
            if not parsed_value.endswith(self.extension):
                return False
        if not os.path.isfile(parsed_value):
            return False
        with open(parsed_value, 'rb') as (fin):
            header_size_bytes = fin.read(4)
            if len(header_size_bytes) != 4:
                return False
            header_size = int.from_bytes(header_size_bytes, 'little')
            if header_size not in (348, 540):
                header_size = int.from_bytes(header_size_bytes, 'big')
            if header_size == 348:
                fin.seek(344)
                magic = fin.read(4)
                return magic == b'n+1\x00'
            else:
                if header_size == 540:
                    magic = fin.read(8)
                    return magic == b'n+2\x00\r\n\x1a\n'
                return False