# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/NiftiImageFile.py
# Compiled at: 2018-05-07 08:52:54
# Size of source mod 2**32: 894 bytes
from fastr.datatypes import TypeGroup

class NiftiImageFile(TypeGroup):
    description = 'NiftiTypeGroup'
    _members = ('NiftiImageFileCompressed', 'NiftiImageFileUncompressed')