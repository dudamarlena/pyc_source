# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/calendar/dayofweek/dayofweek_entity.py
# Compiled at: 2020-01-28 21:04:17
# Size of source mod 2**32: 860 bytes
from foxylib.tools.entity.entity_tool import EntityConfig
from foxylib.tools.locale.locale_tool import LocaleTool
from foxylib.tools.locale.locale_tool import LocaleTool

class DayofweekEntity:

    class Value:
        MONDAY = 'monday'
        TUESDAY = 'tuesday'
        WEDNESDAY = 'wednesday'
        THURSDAY = 'thursday'
        FRIDAY = 'friday'
        SATURDAY = 'saturday'
        SUNDAY = 'sunday'

    V = Value

    @classmethod
    def str2entity_list(cls, str_in, j_config=None):
        locale = EntityConfig.j2locale(j_config)
        lang = LocaleTool.locale2lang(locale)
        if lang == 'ko':
            from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo
            return DayofweekEntityKo.str2entity_list(str_in)
        raise NotImplementedError('Invalid lang: {}'.format(lang))