# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\ContentMapper.py
# Compiled at: 2018-01-18 12:27:37
# Size of source mod 2**32: 1815 bytes
import logging
from .. import CharacterData
from ..Node import Node
from .exceptions import *
from .Mapper import Mapper
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ContentMapper(Mapper):
    __doc__ = "\n        **kwargs**\n\n        enum\n            Enumeration the attribute's value must be from\n        pattern\n            Pattern which the value must match.\n        type\n            Type against which a value must validate\n\n        min\n            The minimum value of the content. Can be numeric or None (the\n            default).\n        max\n            The maximum value of the content. Can be numeric or None (the\n            default).\n    "

    def initialize(self, model):
        from .Model import Model

    def validate(self, model):
        from .Model import Model

    def produce_in(self, el, model, id_):
        from .Model import Model
        logger.debug(str(self) + ' producing ' + str(id_) + ' in ' + str(el))
        el.children.append(CharacterData(str(id_)))