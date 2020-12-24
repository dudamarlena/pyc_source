# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyImageConverter\PyImageConverter.py
# Compiled at: 2019-07-21 10:01:31
# Size of source mod 2**32: 265 bytes
import cv2

def convert(filename, frmt):
    string = filename.split('.')
    img_read = cv2.imread(filename)
    if string[1] == frmt:
        return 'Already in Prescribed Format'
    else:
        return cv2.imwrite(string[0] + '.' + frmt, img_read)