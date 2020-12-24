# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\TotalDigitsElement.py
# Compiled at: 2018-01-18 12:32:24
# Size of source mod 2**32: 1221 bytes
import logging
from ..decorators import *
from .AnnotationElement import AnnotationElement
from .FacetType import FacetType
from .PositiveIntegerType import PositiveIntegerType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='value', type=PositiveIntegerType, required=True)
@attribute(local_name='*')
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0)
class TotalDigitsElement(FacetType):
    pass