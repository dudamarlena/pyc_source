# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\RedefineElement.py
# Compiled at: 2018-01-18 12:31:47
# Size of source mod 2**32: 1772 bytes
import logging
from ..decorators import *
from .AnnotationElement import AnnotationElement
from .AnyTypeType import AnyTypeType
from .AnyUriType import AnyUriType
from .AttributeGroupType import AttributeGroupType
from .ComplexTypeType import ComplexTypeType
from .GroupType import GroupType
from .IdType import IdType
from .SimpleTypeType import SimpleTypeType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='schemaLocation', type=AnyUriType, required=True)
@attribute(local_name='id', type=IdType)
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0, max=None)
@element(local_name='simpleType', list='tags', cls=SimpleTypeType, min=0, max=None)
@element(local_name='complexType', list='tags', cls=ComplexTypeType, min=0, max=None)
@element(local_name='group', list='tags', cls=GroupType, min=0, max=None)
@element(local_name='attributeGroup', list='tags', cls=AttributeGroupType, min=0, max=None)
class RedefineElement(AnyTypeType):
    pass