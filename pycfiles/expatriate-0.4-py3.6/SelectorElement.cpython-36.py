# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\SelectorElement.py
# Compiled at: 2018-01-18 12:31:57
# Size of source mod 2**32: 1054 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .SelectorXPath import SelectorXPath
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='xpath', type=SelectorXPath, required=True)
class SelectorElement(AnnotatedType):
    pass