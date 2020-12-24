# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DigiPathAI/helpers/convert_to_pyramidal.py
# Compiled at: 2019-11-09 07:15:25
# Size of source mod 2**32: 1309 bytes
import os, sys, numpy as np, json, glob, time

def create_pyramidal_img(img_path, output_image_path):
    """ Convert normal image to pyramidal image.
    Parameters
    -------
    img_path: str
        Absolute path of Whole slide image path (absolute path is needed)
    output_image_path: str
        Absolute path of of the saved the generated pyramidal image with extension tiff,

    Returns
    -------
    status: int
        The status of the pyramidal image generation (0 stands for success)
    Notes
    -------
    ImageMagick need to be preinstalled to use this function.
    >>> sudo apt-get install imagemagick
    Examples
    --------
    >>> img_path = os.path.join(PRJ_PATH, "test/data/Images/CropBreastSlide.tif")
    >>> save_dir = os.path.join(PRJ_PATH, "test/data/Slides")
    >>> status = pyramid.create_pyramidal_img(img_path, save_dir)
    >>> assert status == 0
    """
    convert_cmd = 'convert ' + os.path.abspath(img_path)
    convert_option = ' -compress LZW -define tiff:tile-geometry=256x256 ptif:'
    img_name = os.path.basename(img_path)
    convert_dst = output_image_path
    status = os.system(convert_cmd + convert_option + convert_dst)
    return status