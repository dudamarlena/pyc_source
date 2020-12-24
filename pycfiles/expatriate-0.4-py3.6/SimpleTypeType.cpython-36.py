# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\SimpleTypeType.py
# Compiled at: 2018-01-18 12:32:12
# Size of source mod 2**32: 1711 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .NCNameType import NCNameType
from .RestrictionType import RestrictionType
from .UnionElement import UnionElement
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@element(local_name='restriction', list='tags', cls=RestrictionType, min=0)
@element(local_name='list', list='tags', cls=('expatriate.model.xs.ListElement', 'ListElement'), min=0)
@element(local_name='union', list='tags', cls=UnionElement, min=0)
@attribute(local_name='final', enum=['#all', 'list', 'union', 'restriction'])
@attribute(local_name='name', type=NCNameType)
@attribute(local_name='*')
class SimpleTypeType(AnnotatedType):

    def stub(self, path, schema):
        class_name = ''.join(cap_first(w) for w in self.name.split('_'))
        if not class_name.endswith('Type'):
            class_name = class_name + 'Type'
        super().stub(path, schema, class_name)