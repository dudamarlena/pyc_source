# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/videogame/overwatch/tier/overwatch_tier.py
# Compiled at: 2020-02-12 00:10:09
# Size of source mod 2**32: 1763 bytes
import os
from functools import lru_cache
from foxylib.tools.collections.collections_tool import filter2singleton, vwrite_no_duplicate_key, merge_dicts
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.json.json_tool import jdown
from foxylib.tools.json.yaml_tool import YAMLTool
FILE_PATH = os.path.abspath(__file__)
FILE_DIR = os.path.dirname(FILE_PATH)

class OverwatchTier:

    class Name:
        BRONZE = 'bronze'
        SILVER = 'silver'
        GOLD = 'gold'
        PLATINUM = 'platinum'
        DIAMOND = 'diamond'
        MASTER = 'master'
        GRANDMASTER = 'grandmaster'
        TOP500 = 'top500'

    class Field:
        NAME = 'name'
        IMAGE_URL = 'image_url'
        TEXT = 'text'

    F = Field

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def j_yaml(cls):
        filepath = os.path.join(FILE_DIR, 'overwatch_tier.yaml')
        j = YAMLTool.filepath2j(filepath)
        return j

    @classmethod
    def j_list_all(cls):
        return cls.j_yaml()

    @classmethod
    def j2name(cls, j):
        return j[cls.F.NAME]

    @classmethod
    def j_lang2text(cls, j, lang):
        return jdown(j, [cls.F.TEXT, lang])

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def h_name2j(cls):
        h = merge_dicts([{cls.j2name(j): j} for j in cls.j_list_all()],
          vwrite=vwrite_no_duplicate_key)
        return h

    @classmethod
    def name2j(cls, name):
        return cls.h_name2j().get(name)

    @classmethod
    def name_lang2text(cls, name, lang):
        j = cls.h_name2j(name)
        if not j:
            return
        text = cls.j_lang2text(j, name)
        return text