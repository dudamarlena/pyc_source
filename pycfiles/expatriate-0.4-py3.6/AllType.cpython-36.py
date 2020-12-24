# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AllType.py
# Compiled at: 2018-01-18 12:28:05
# Size of source mod 2**32: 1325 bytes
import logging
from ..decorators import *
from .AnnotationElement import AnnotationElement
from .ElementType import ElementType
from .GroupType import GroupType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='minOccurs', enum=['0', '1'], default='1')
@attribute(local_name='maxOccurs', enum=['1'], default='1')
@attribute(local_name='*')
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0)
@element(local_name='element', list='tags', cls=ElementType, min=0, max=None)
class AllType(GroupType):
    pass