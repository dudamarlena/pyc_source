# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/NrrdImageFile.py
# Compiled at: 2018-07-03 10:02:09
# Size of source mod 2**32: 829 bytes
from fastr.datatypes import URLType

class NrrdImageFile(URLType):
    description = 'Nrrd Image File format'
    extension = 'nrrd'