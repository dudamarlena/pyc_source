# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AnyElement.py
# Compiled at: 2018-01-18 12:28:22
# Size of source mod 2**32: 1454 bytes
import logging
from ..decorators import *
from .AllNniType import AllNniType
from .NonNegativeIntegerType import NonNegativeIntegerType
from .WildcardType import WildcardType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='minOccurs', type=NonNegativeIntegerType, default=1)
@attribute(local_name='maxOccurs', type=AllNniType, default=1)
class AnyElement(WildcardType):

    def get_defs(self, schema):
        model_map = {'elements':[],  'attributes':{}}
        tag = {'tag_name':'*', 
         'min':0}
        if self.namespace != '##any':
            tag['namespace'] = self.namespace
        model_map['elements'].append(tag)
        return model_map