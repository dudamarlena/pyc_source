# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/Visual/Pictures.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = ' Captcha.Visual.Pictures\n\nRandom collections of images\n'
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