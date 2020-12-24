# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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