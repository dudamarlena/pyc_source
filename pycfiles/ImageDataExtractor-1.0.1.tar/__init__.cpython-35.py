# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edward/github/ImageDataExtractor/imagedataextractor/__init__.py
# Compiled at: 2019-05-20 06:43:25
# Size of source mod 2**32: 481 bytes
"""
ImageDataExtractor
~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
__title__ = 'ImageDataExtractor'
__version__ = '0.0.1'
__author__ = 'Karim Mukaddem'
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
from .extract import extract_document, extract_documents, extract_image, extract_images