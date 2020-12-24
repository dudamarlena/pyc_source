# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\pytesser3\util.py
# Compiled at: 2016-09-22 04:55:59
# Size of source mod 2**32: 669 bytes
"""Utility functions for processing images for delivery to Tesseract"""
import os

def image_to_scratch(im, scratch_image_name):
    """Saves image in memory to scratch file.  .bmp format will be read correctly by Tesseract"""
    im.save(scratch_image_name, dpi=(200, 200))


def retrieve_text(scratch_text_name_root):
    inf = open(scratch_text_name_root + '.txt')
    text = inf.read()
    inf.close()
    return text


def perform_cleanup(scratch_image_name, scratch_text_name_root):
    """Clean up temporary files from disk"""
    for name in (scratch_image_name, scratch_text_name_root + '.txt', 'tesseract.log'):
        try:
            os.remove(name)
        except OSError:
            pass