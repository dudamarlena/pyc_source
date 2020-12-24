# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dir2html/get_images.py
# Compiled at: 2018-11-21 04:57:05
# Size of source mod 2**32: 560 bytes
import os, imghdr

def get_images(directory):
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                full_path = '{}/{}'.format(os.path.realpath(root), file)
                img_type = imghdr.what(full_path)
                if img_type is not None:
                    images.append(full_path)
            except IOError as e:
                print('Error: {}'.format(e))

    return images