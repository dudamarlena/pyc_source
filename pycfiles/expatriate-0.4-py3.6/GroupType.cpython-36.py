# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\GroupType.py
# Compiled at: 2018-01-18 12:30:20
# Size of source mod 2**32: 2105 bytes
import logging
from ..decorators import *
from .AllNniType import AllNniType
from .AnnotatedType import AnnotatedType
from .AnyElement import AnyElement
from .NCNameType import NCNameType
from .NonNegativeIntegerType import NonNegativeIntegerType
from .QNameType import QNameType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='minOccurs', type=NonNegativeIntegerType, default=1)
@attribute(local_name='maxOccurs', type=AllNniType, default=1)
@attribute(local_name='*')
@element(local_name='any', list='tags', cls=AnyElement, min=0, max=None)
@element(local_name='element', list='tags', cls=('expatriate.model.xs.ElementType',
                                                 'ElementType'),
  min=0,
  max=None)
@element(local_name='group', list='tags', cls=('expatriate.model.xs.GroupType', 'GroupType'),
  min=0,
  max=None)
@element(local_name='all', list='tags', cls=('expatriate.model.xs.AllType', 'AllType'),
  min=0,
  max=None)
@element(local_name='choice', list='tags', cls=('expatriate.model.xs.ChoiceElement',
                                                'ChoiceElement'),
  min=0,
  max=None)
@element(local_name='sequence', list='tags', cls=('expatriate.model.xs.GroupType',
                                                  'GroupType'),
  min=0,
  max=None)
class GroupType(AnnotatedType):
    pass