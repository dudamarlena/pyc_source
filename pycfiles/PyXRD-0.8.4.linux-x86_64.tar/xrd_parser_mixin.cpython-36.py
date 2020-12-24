# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/xrd_parser_mixin.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 420 bytes
from .xrd_data_object import XRDDataObject

class XRDParserMixin(object):
    __doc__ = '\n        This is a mixin class which provides common functionality and attributes\n        for XRD-data parser classes.\n    '
    data_object_type = XRDDataObject