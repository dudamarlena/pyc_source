# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\KeybaseType.py
# Compiled at: 2018-01-18 12:30:51
# Size of source mod 2**32: 1271 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .FieldElement import FieldElement
from .NCNameType import NCNameType
from .SelectorElement import SelectorElement
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', type=NCNameType, required=True)
@element(local_name='selector', list='tags', cls=SelectorElement)
@element(local_name='field', list='tags', cls=FieldElement, min=1, max=None)
class KeybaseType(AnnotatedType):
    pass