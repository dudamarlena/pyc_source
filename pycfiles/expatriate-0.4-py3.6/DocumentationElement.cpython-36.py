# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\xs\DocumentationElement.py
# Compiled at: 2018-01-18 12:29:11
# Size of source mod 2**32: 1202 bytes
import logging
from ..decorators import *
from ..Model import Model
from .AnyUriType import AnyUriType
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@attribute(local_name='*')
@attribute(local_name='source', type=AnyUriType)
@element(local_name='*', min=0, max=None)
class DocumentationElement(Model):

    def get_defs(self, schema, top_level):
        model_map = {'elements':[],  'attributes':{}}
        return model_map