# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/botcore/util/image_util.py
# Compiled at: 2018-04-01 06:36:57
# Size of source mod 2**32: 171 bytes


def convert_image_to_bytes(image):
    with open(image, 'rb') as (imageFile):
        file = imageFile.read()
        bytes_result = bytearray(file)
    return bytes_result