# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\NotationElement.py
# Compiled at: 2018-01-18 12:31:32
# Size of source mod 2**32: 1213 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AnyUriType import AnyUriType
from .NCNameType import NCNameType
from .TokenType import TokenType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', type=NCNameType, required=True)
@attribute(local_name='public', type=TokenType)
@attribute(local_name='system', type=AnyUriType)
class NotationElement(AnnotatedType):
    pass