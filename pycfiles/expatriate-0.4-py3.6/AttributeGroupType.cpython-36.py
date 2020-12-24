# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AttributeGroupType.py
# Compiled at: 2018-01-18 12:28:35
# Size of source mod 2**32: 1575 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AttributeType import AttributeType
from .NCNameType import NCNameType
from .QNameType import QNameType
from .WildcardType import WildcardType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='*')
@element(local_name='attribute', list='tags', cls=('expatriate.model.xs.AttributeType',
                                                   'AttributeType'),
  min=0,
  max=None)
@element(local_name='attributeGroup', list='tags', cls=('expatriate.model.xs.AttributeGroupType',
                                                        'AttributeGroupType'),
  min=0,
  max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class AttributeGroupType(AnnotatedType):
    pass