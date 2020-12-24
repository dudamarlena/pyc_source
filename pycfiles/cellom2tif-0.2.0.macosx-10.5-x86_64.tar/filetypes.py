# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nuneziglesiasj/anaconda/envs/bioformats/lib/python2.7/site-packages/cellom2tif/filetypes.py
# Compiled at: 2013-07-28 00:05:41


def is_cellomics_image(fn):
    """Determine whether a file is a Cellomics image.

    Parameters
    ----------
    fn : string
        The filename of the file in question.

    Returns
    -------
    is_cellom : bool
        True if the filename points to a Cellomics image.
    """
    is_cellom = fn.endswith('.C01') or fn.endswith('.c01')
    return is_cellom


def is_cellomics_mask(fn):
    """Determine whether a file is a Cellomics mask image.

    Parameters
    ----------
    fn : string
        The filename.

    Returns
    -------
    is_mask : bool
        True if the filename points to a Cellomics mask image.
    """
    is_mask = fn.endswith('o1.C01') or fn.endswith('o1.c01')
    return is_mask