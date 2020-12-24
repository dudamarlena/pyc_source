# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/bpatch.py
# Compiled at: 2019-03-03 18:49:22
from bsdiff import Patch
import os, sys, bz2
from array import array
import struct
from six import StringIO

def patch(old_file_name, new_file_name, patch_file_name):
    patch_file = open(patch_file_name, 'rb')
    patch_file.read(8)
    compressed_control_len = offtin(patch_file.read(8))
    compressed_diff_len = offtin(patch_file.read(8))
    new_file_len = offtin(patch_file.read(8))
    compressed_control_block = patch_file.read(compressed_control_len)
    compressed_diff_block = patch_file.read(compressed_diff_len)
    compressed_extra_block = patch_file.read()
    control_stream = StringIO(bz2.decompress(compressed_control_block))
    diff_string = bz2.decompress(compressed_diff_block)
    extra_string = bz2.decompress(compressed_extra_block)
    control_tuples_list = []
    while True:
        r = control_stream.read(8)
        if not r:
            break
        x = offtin(r)
        y = offtin(control_stream.read(8))
        z = offtin(control_stream.read(8))
        control_tuples_list.append((x, y, z))

    old_data = open(old_file_name, 'rb').read()
    new_data = Patch(old_data, new_file_len, control_tuples_list, diff_string, extra_string)
    new_file = open(new_file_name, 'wb')
    new_file.write(new_data)


def offtin(buf):
    s = ord(buf[7])
    y = (s & 127) << 56
    y += ord(buf[6]) << 48
    y += ord(buf[5]) << 40
    y += ord(buf[4]) << 32
    y += ord(buf[3]) << 24
    y += ord(buf[2]) << 16
    y += ord(buf[1]) << 8
    y += ord(buf[0])
    if s & 128:
        y = -y
    return y


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'bpatch: usage: python bpatch.py oldfile newfile patchfile'
    else:
        old_file_name = sys.argv[1]
        new_file_name = sys.argv[2]
        patch_file_name = sys.argv[3]
        patch(old_file_name, new_file_name, patch_file_name)