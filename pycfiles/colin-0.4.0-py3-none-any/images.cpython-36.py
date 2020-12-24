# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/checks/images.py
# Compiled at: 2018-09-04 03:34:18
# Size of source mod 2**32: 830 bytes
from .abstract_check import AbstractCheck

class ImageAbstractCheck(AbstractCheck):
    check_type = 'image'


class FilesystemAbstractCheck(AbstractCheck):
    pass