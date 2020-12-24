# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ImageMetaTag/__init__.py
# Compiled at: 2017-12-05 07:30:14
"""
ImageMetaTag is a python package built around a wrapper for
`savefig <http://matplotlib.org/api/pyplot_api.html?highlight=savefig#matplotlib.pyplot.savefig>`_
in
`matplotlib <http://matplotlib.org/>`_, which adds metadata tags to supported image file formats.

Once the images have been tagged, it can also be used to manage an
`SQL database <https://docs.python.org/2/library/sqlite3.html>`_ of images and their metadata.
The image metadata can be used to produce an
:class:`ImageMetaTag.ImageDict` object: a structured/heirachical dictionary of dictionaries
which can be used to easily create web pages to present large numbers of images.

As the image metadata tagging process involves reading the image using the Image library,
a few common image post-processing options are included such as cropping, logo addition and
colour palette manipulation to reduce filesizes.

.. moduleauthor:: Malcolm Brooks https://github.com/malcolmbrooks

(C) Crown copyright Met Office. All rights reserved.
Released under BSD 3-Clause License. See LICENSE for more details.
"""
__version__ = '0.6.9'
__documentation__ = 'http://scitools-incubator.github.io/image-meta-tag/build/html/'
META_IMG_FORMATS = [
 'png']
POSTPROC_IMG_FORMATS = [
 'png']
DEFAULT_DB_TIMEOUT = 6
DEFAULT_DB_ATTEMPTS = 20
from ImageMetaTag.savefig import savefig, image_file_postproc
from ImageMetaTag.img_dict import ImageDict, readmeta_from_image, dict_heirachy_from_list, dict_split, simple_dict_filter, check_for_required_keys
import ImageMetaTag.webpage, ImageMetaTag.db