# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\ComplexTypeType.py
# Compiled at: 2018-01-18 12:28:54
# Size of source mod 2**32: 2779 bytes
import logging, os.path
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AttributeGroupType import AttributeGroupType
from .AttributeType import AttributeType
from .BooleanType import BooleanType
from .ChoiceElement import ChoiceElement
from .ComplexContentElement import ComplexContentElement
from .GroupType import GroupType
from .NCNameType import NCNameType
from .SimpleContentElement import SimpleContentElement
from .WildcardType import WildcardType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='mixed', type=BooleanType, default=False)
@attribute(local_name='abstract', type=BooleanType, default=False)
@attribute(local_name='final', enum=['#all', 'extension', 'restriction'])
@attribute(local_name='block', enum=['#all', 'extension', 'restriction'])
@attribute(local_name='*')
@element(local_name='simpleContent', list='tags', cls=SimpleContentElement, min=0, max=None)
@element(local_name='complexContent', list='tags', cls=ComplexContentElement, min=0, max=None)
@element(local_name='group', list='tags', cls=GroupType, min=0)
@element(local_name='all', list='tags', cls=('expatriate.model.xs.AllType', 'AllType'),
  min=0)
@element(local_name='choice', list='tags', cls=ChoiceElement, min=0)
@element(local_name='sequence', list='tags', cls=GroupType, min=0)
@element(local_name='attribute', list='tags', cls=AttributeType, min=0, max=None)
@element(local_name='attributeGroup', list='tags', cls=AttributeGroupType, min=0, max=None)
@element(local_name='anyAttribute', list='tags', cls=WildcardType, min=0)
class ComplexTypeType(AnnotatedType):

    def stub(self, path, schema):
        class_name = ''.join(cap_first(w) for w in self.name.split('_'))
        if not class_name.endswith('Type'):
            class_name = class_name + 'Type'
        super().stub(path, schema, class_name)