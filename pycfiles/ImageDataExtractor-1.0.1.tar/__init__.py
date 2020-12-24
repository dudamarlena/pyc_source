# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: imagedataextractor/__init__.py
# Compiled at: 2019-05-16 11:15:11
"""
ImageDataExtractor
~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging
__title__ = b'ImageDataExtractor'
__version__ = b'0.0.1'
__author__ = b'Karim Mukaddem'
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
from .extract import extract_document, extract_documents, extract_image, extract_images