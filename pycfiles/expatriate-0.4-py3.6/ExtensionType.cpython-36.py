# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\ExtensionType.py
# Compiled at: 2018-01-18 12:29:58
# Size of source mod 2**32: 2172 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AttributeGroupType import AttributeGroupType
from .AttributeType import AttributeType
from .ChoiceElement import ChoiceElement
from .GroupType import GroupType
from .QNameType import QNameType
from .WildcardType import WildcardType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='base', type=QNameType, required=True)
@element(local_name='group', list='tags', cls=GroupType, min=0)
@element(local_name='all', list='tags', cls=('expatriate.model.xs.AllType', 'AllType'),
  min=0)
@element(local_name='choice', list='tags', cls=ChoiceElement, min=0)
@element(local_name='sequence', list='tags', cls=GroupType, min=0)
@element(local_name='attribute', list='tags', cls=AttributeType, min=0, max=None)
@element(local_name='attributeGroup', list='tags', cls=AttributeGroupType, min=0, max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class ExtensionType(AnnotatedType):

    def get_defs(self, schema, top_level):
        logger.debug('Base: ' + self.base)
        base_ns, base_name = [self.base.partition(':')[i] for i in (0, 2)]
        top_level.set_super_module(base_ns)
        top_level.set_super_class(base_name)
        return super().get_defs(schema, top_level)