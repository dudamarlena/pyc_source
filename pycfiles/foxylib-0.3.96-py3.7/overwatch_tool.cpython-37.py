# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/videogame/overwatch/overwatch_tool.py
# Compiled at: 2020-02-07 13:26:24
# Size of source mod 2**32: 788 bytes
from foxylib.tools.collections.collections_tool import zip_strict, lzip_strict
from foxylib.tools.locale.locale_tool import LocaleTool
from foxylib.tools.json.json_tool import jdown

class OverwatchTool:

    @classmethod
    def tier_list(cls):
        return ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster', 'Top500']

    @classmethod
    def lang2tier_value_name_list(cls, lang):
        v_list = cls.tier_list()
        if not lang or lang == 'en':
            return [(x, x) for x in v_list]
        if lang == 'ko':
            name_list = [
             '브론즈', '실버', '골드', '플래티넘', '다이아몬드', '마스터', '그랜드마스터', '랭커']
            return lzip_strict(v_list, name_list)
        raise NotImplementedError({'lang': lang})