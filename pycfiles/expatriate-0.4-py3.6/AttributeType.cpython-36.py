# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\AttributeType.py
# Compiled at: 2018-01-18 12:28:38
# Size of source mod 2**32: 1634 bytes
import logging
from . import FORM_CHOICE_ENUMERATION
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .NCNameType import NCNameType
from .QNameType import QNameType
from .SimpleTypeType import SimpleTypeType
from .StringType import StringType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', type=NCNameType)
@attribute(local_name='ref', type=QNameType)
@attribute(local_name='type', type=QNameType)
@attribute(local_name='use', enum=['prohibited', 'optional', 'required'], default='optional')
@attribute(local_name='default', type=StringType)
@attribute(local_name='fixed', type=StringType)
@attribute(local_name='form', enum=FORM_CHOICE_ENUMERATION)
@attribute(local_name='*')
@element(local_name='simpleType', list='tags', cls=SimpleTypeType, min=0)
class AttributeType(AnnotatedType):
    pass