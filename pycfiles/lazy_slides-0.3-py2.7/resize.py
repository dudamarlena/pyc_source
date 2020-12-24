# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/manipulation/resize.py
# Compiled at: 2012-03-18 03:50:21
import logging, Image
log = logging.getLogger(__name__)

def resize(infilename, outfilename, new_size):
    """Resize an image file.

    :param infilename: The input image file name.
    :param outfilename: The output image file name.
    :param new_size: A tuple (width, height) of the new image size.
    """
    log.info(('Resizing {} to {}. New size = {}').format(infilename, outfilename, new_size))
    im = Image.open(infilename)
    im_resized = im.resize(new_size)
    im_resized.save(outfilename)
    return outfilename