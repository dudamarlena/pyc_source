# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/checks/images.py
# Compiled at: 2018-09-04 03:34:18
# Size of source mod 2**32: 830 bytes
from .abstract_check import AbstractCheck

class ImageAbstractCheck(AbstractCheck):
    check_type = 'image'


class FilesystemAbstractCheck(AbstractCheck):
    pass