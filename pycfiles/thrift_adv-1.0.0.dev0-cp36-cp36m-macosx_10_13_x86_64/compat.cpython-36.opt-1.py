# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /thrift/compat.py
# Compiled at: 2018-09-11 21:54:05
# Size of source mod 2**32: 1315 bytes
import sys
if sys.version_info[0] == 2:
    from cStringIO import StringIO as BufferIO

    def binary_to_str(bin_val):
        return bin_val


    def str_to_binary(str_val):
        return str_val


    def byte_index(bytes_val, i):
        return ord(bytes_val[i])


else:
    from io import BytesIO as BufferIO

    def binary_to_str(bin_val):
        return bin_val.decode('utf8')


    def str_to_binary(str_val):
        return bytes(str_val, 'utf8')


    def byte_index(bytes_val, i):
        return bytes_val[i]