# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nuneziglesiasj/anaconda/envs/bioformats/lib/python2.7/site-packages/cellom2tif/__init__.py
# Compiled at: 2014-06-27 03:55:17
"""cellom2tif package: functions to convert Cellomics images to TIFF.
"""
from cellom2tif import read_image, convert_files
from filetypes import is_cellomics_image, is_cellomics_mask
__all__ = [
 'read_image', 'convert_files',
 'is_cellomics_image', 'is_cellomics_mask']