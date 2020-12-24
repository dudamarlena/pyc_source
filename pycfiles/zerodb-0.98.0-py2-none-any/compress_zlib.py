# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/transform/compress_zlib.py
# Compiled at: 2016-03-08 18:12:41
import zlib
from .compress_common import CommonCompressor
zlib_compressor = CommonCompressor(name='zlib', compress=zlib.compress, decompress=zlib.decompress, args=[2])