# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xshfp\HasPropertyElement.py
# Compiled at: 2018-01-18 12:32:56
# Size of source mod 2**32: 1178 bytes
import logging
from . import PROPERTY_NAME_ENUMERATION
from ..decorators import *
from ..Model import Model
from ..xs.NormalizedStringType import NormalizedStringType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='name', required=True, enum=PROPERTY_NAME_ENUMERATION)
@attribute(local_name='value', required=True, type=NormalizedStringType)
class HasPropertyElement(Model):
    pass