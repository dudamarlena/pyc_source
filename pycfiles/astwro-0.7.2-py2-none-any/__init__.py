# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michal/projects/astwro/astwro/sampledata/__init__.py
# Compiled at: 2017-08-16 18:43:07
"""
Module contains sample FITS file and other daophot files for testing
"""

def fits_image():
    """path of FITS image of NGC6871"""
    return __sampledata('NGC6871.fits')


def coo_file():
    """path of `coo` file for :py:func:`fits_image()`"""
    return __sampledata('NGC6871.coo')


def lst_file():
    """path of `lst` file for :py:func:`fits_image()` """
    return __sampledata('NGC6871.lst')


def ap_file():
    """path of `ap` file for :py:func:`fits_image()`"""
    return __sampledata('NGC6871.ap')


def psf_file():
    """path of `psf` file for :py:func:`fits_image()`"""
    return __sampledata('NGC6871.psf')


def als_file():
    """path of `als` file for :py:func:`fits_image()`"""
    return __sampledata('NGC6871.als')


def nei_file():
    """path of `nei` file for :py:func:`fits_image()`"""
    return __sampledata('NGC6871.nei')


def err_file():
    return __sampledata('i.err')


def head_file():
    """patch of sample ASCII fits header file"""
    return __sampledata('astrometry.head')


def __sampledata(filename):
    import os
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)