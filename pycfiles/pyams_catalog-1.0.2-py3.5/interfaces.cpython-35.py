# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_catalog/interfaces.py
# Compiled at: 2020-02-21 06:54:32
# Size of source mod 2**32: 1208 bytes
"""PyAMS_catalog.interfaces module

This module provides all package interfaces.
"""
from zope.interface import Interface
NLTK_LANGUAGES = {'da': 'danish', 
 'nl': 'dutch', 
 'en': 'english', 
 'fi': 'finnish', 
 'fr': 'french', 
 'de': 'german', 
 'hu': 'hungarian', 
 'it': 'italian', 
 'no': 'norwegian', 
 'po': 'porter', 
 'pt': 'portuguese', 
 'ro': 'romanian', 
 'ru': 'russian', 
 'es': 'spanish', 
 'sv': 'swedish'}
NO_RESOLUTION = 6
SECOND_RESOLUTION = 5
MINUTE_RESOLUTION = 4
HOUR_RESOLUTION = 3
DATE_RESOLUTION = 2
MONTH_RESOLUTION = 1
YEAR_RESOLUTION = 0

class INoAutoIndex(Interface):
    __doc__ = "Marker interface for objects which shouldn't be automatically indexed"