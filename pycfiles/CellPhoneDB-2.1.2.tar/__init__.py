# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/nuneziglesiasj/anaconda/envs/bioformats/lib/python2.7/site-packages/cellom2tif/__init__.py
# Compiled at: 2014-06-27 03:55:17
__doc__ = 'cellom2tif package: functions to convert Cellomics images to TIFF.\n'
from cellom2tif import read_image, convert_files
from filetypes import is_cellomics_image, is_cellomics_mask
__all__ = [
 'read_image', 'convert_files',
 'is_cellomics_image', 'is_cellomics_mask']