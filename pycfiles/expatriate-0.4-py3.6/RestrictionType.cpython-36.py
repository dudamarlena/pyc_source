# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\RestrictionType.py
# Compiled at: 2018-01-18 12:31:51
# Size of source mod 2**32: 3466 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .ChoiceElement import ChoiceElement
from .FacetType import FacetType
from .GroupType import GroupType
from .PatternElement import PatternElement
from .QNameType import QNameType
from .TotalDigitsElement import TotalDigitsElement
from .WhitespaceElement import WhitespaceElement
from .WildcardType import WildcardType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='base', type=QNameType)
@element(local_name='group', list='tags', cls=GroupType, min=0)
@element(local_name='all', list='tags', cls=('expatriate.model.xs.AllType', 'AllType'),
  min=0)
@element(local_name='choice', list='tags', cls=ChoiceElement, min=0)
@element(local_name='sequence', list='tags', cls=GroupType, min=0)
@element(local_name='simpleType', list='tags', cls=('expatriate.model.xs.SimpleTypeType',
                                                    'SimpleTypeType'),
  min=0)
@element(local_name='minExclusive', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='minInclusive', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='maxExclusive', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='maxInclusive', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='totalDigits', list='tags', cls=TotalDigitsElement, min=0, max=None)
@element(local_name='fractionDigits', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='length', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='minLength', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='maxLength', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='enumeration', list='tags', cls=FacetType, min=0, max=None)
@element(local_name='whiteSpace', list='tags', cls=WhitespaceElement, min=0, max=None)
@element(local_name='pattern', list='tags', cls=PatternElement, min=0, max=None)
@element(local_name='attribute', list='tags', cls=('expatriate.model.xs.AttributeType',
                                                   'AttributeType'),
  min=0,
  max=None)
@element(local_name='attributeGroup', list='tags', cls=('expatriate.model.xs.AttributeGroupType',
                                                        'AttributeGroupType'),
  min=0,
  max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class RestrictionType(AnnotatedType):

    def get_defs(self, schema, top_level):
        logger.debug('Base: ' + self.base)
        base_ns, base_name = [self.base.partition(':')[i] for i in (0, 2)]
        top_level.set_super_module(base_ns)
        top_level.set_super_class(base_name)
        return super().get_defs(schema, top_level)