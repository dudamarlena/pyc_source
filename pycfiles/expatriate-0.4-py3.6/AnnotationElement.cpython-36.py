# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AnnotationElement.py
# Compiled at: 2018-01-18 12:28:16
# Size of source mod 2**32: 1287 bytes
import logging
from ..decorators import *
from .AnyTypeType import AnyTypeType
from .AppinfoElement import AppinfoElement
from .DocumentationElement import DocumentationElement
from .IdType import IdType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='id', type=IdType)
@element(local_name='appinfo', list='tags', cls=AppinfoElement, min=0, max=None)
@element(local_name='documentation', list='tags', cls=DocumentationElement, min=0, max=None)
class AnnotationElement(AnyTypeType):
    pass