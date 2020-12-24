# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\UnionElement.py
# Compiled at: 2018-01-18 12:32:27
# Size of source mod 2**32: 1167 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .QNameType import QNameType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='memberTypes', type=QNameType)
@element(local_name='simpleType', list='tags', cls=('expatriate.model.xs.SimpleTypeType',
                                                    'SimpleTypeType'),
  min=0,
  max=None)
class UnionElement(AnnotatedType):
    pass