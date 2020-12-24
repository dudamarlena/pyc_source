# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/cardinal/cardinal_entity.py
# Compiled at: 2020-01-28 21:04:17
# Size of source mod 2**32: 1127 bytes
import os, re
from functools import lru_cache
from future.utils import lmap
from foxylib.tools.entity.entity_tool import Entity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.regex.regex_tool import RegexTool
FILE_PATH = os.path.realpath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class CardinalEntity:

    @classmethod
    def rstr(cls):
        rstr_multidigit = '[1-9][0-9]+'
        rstr_onedigit = '[0-9]'
        rstr_number = RegexTool.rstr_list2or([rstr_multidigit, rstr_onedigit])
        return rstr_number

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern(cls):
        return re.compile(cls.rstr(), re.I)

    @classmethod
    def m2entity(cls, m):
        text = m.group()
        return {Entity.F.SPAN: m.span(), 
         Entity.F.TEXT: text, 
         Entity.F.VALUE: int(text)}

    @classmethod
    def str2entity_list(cls, str_in):
        p = cls.pattern()
        m_list = list(p.finditer(str_in))
        entity_list = lmap(cls.m2entity, m_list)
        return entity_list