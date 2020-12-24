# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\SimpleContentElement.py
# Compiled at: 2018-01-18 12:32:09
# Size of source mod 2**32: 1188 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .ExtensionType import ExtensionType
from .RestrictionType import RestrictionType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@element(local_name='restriction', list='tags', cls=RestrictionType, min=0)
@element(local_name='extension', list='tags', cls=ExtensionType, min=0)
class SimpleContentElement(AnnotatedType):
    pass