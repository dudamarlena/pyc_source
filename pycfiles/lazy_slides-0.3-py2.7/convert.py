# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lazy_slides/manipulation/convert.py
# Compiled at: 2012-03-18 03:50:21
import logging, os, Image
log = logging.getLogger(__name__)

def convert(infilename, target_type='png'):
    """Convert an image from one type to another.

    This uses PIL to convert an input file into another
    type.

    :param infilename: The name of the file to convert.
    :param target_type: The new image type to save as.
    """
    outfilename = ('{}.{}').format(os.path.splitext(infilename)[0], target_type)
    log.info(('Converting {} to {}.').format(infilename, outfilename))
    im = Image.open(infilename)
    im.save(outfilename)
    return outfilename