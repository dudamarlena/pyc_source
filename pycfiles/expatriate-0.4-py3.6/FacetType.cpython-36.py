# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\FacetType.py
# Compiled at: 2018-01-18 12:30:02
# Size of source mod 2**32: 1373 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AnySimpleType import AnySimpleType
from .BooleanType import BooleanType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='value', required=True, type=AnySimpleType)
@attribute(local_name='fixed', type=BooleanType, default=False)
@attribute(local_name='*')
class FacetType(AnnotatedType):

    def get_defs(self, schema, top_level):
        if self.tag_name == 'enumeration':
            top_level.append_value_enumeration(self.value)
        return super().get_defs(schema, top_level)