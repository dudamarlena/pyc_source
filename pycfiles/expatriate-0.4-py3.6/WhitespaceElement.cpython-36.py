# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\WhitespaceElement.py
# Compiled at: 2018-01-18 12:32:43
# Size of source mod 2**32: 1182 bytes
import logging
from ..decorators import *
from .AnnotationElement import AnnotationElement
from .FacetType import FacetType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='value', required=True, enum=['preserve', 'replace', 'collapse'])
@attribute(local_name='*')
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0)
class WhitespaceElement(FacetType):
    pass