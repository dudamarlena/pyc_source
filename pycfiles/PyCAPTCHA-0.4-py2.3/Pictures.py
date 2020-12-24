# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Visual/Pictures.py
# Compiled at: 2006-02-05 00:25:47
""" Captcha.Visual.Pictures

Random collections of images
"""
from Captcha import File
import Image

class ImageFactory(File.RandomFileFactory):
    """A factory that generates random images from a list"""
    __module__ = __name__
    extensions = [
     '.png', '.jpeg']
    basePath = 'pictures'


abstract = ImageFactory('abstract')
nature = ImageFactory('nature')