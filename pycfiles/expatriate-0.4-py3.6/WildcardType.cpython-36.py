# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\WildcardType.py
# Compiled at: 2018-01-18 12:32:46
# Size of source mod 2**32: 1447 bytes
import logging
from ..decorators import *
from .AnnotatedType import AnnotatedType
from .AnnotationElement import AnnotationElement
from .NamespaceListType import NamespaceListType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='namespace', type=NamespaceListType, default='##any')
@attribute(local_name='processContents', enum=['skip', 'lax', 'strict'], default='strict')
@attribute(local_name='*')
@element(local_name='annotation', list='tags', cls=AnnotationElement, min=0)
@element(local_name='element', list='tags', cls=('expatriate.model.xs.ElementType',
                                                 'ElementType'),
  min=0,
  max=None)
class WildcardType(AnnotatedType):
    pass