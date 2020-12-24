# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/calendar/dayofweek/locale/ko/dayofweek_span_entity_ko.py
# Compiled at: 2020-01-28 21:04:17
# Size of source mod 2**32: 6624 bytes
import logging, re
from functools import lru_cache
from itertools import chain
from future.utils import lmap, lfilter
from foxylib.tools.collections.collections_tool import vwrite_no_duplicate_key, merge_dicts, lchain, luniq, IterTool, ListTool, llmap, f_iter2f_list, vwrite_overwrite, tmap
from foxylib.tools.entity.calendar.dayofweek.dayofweek_entity import DayofweekEntity
from foxylib.tools.entity.calendar.dayofweek.locale.ko.dayofweek_entity_ko import DayofweekEntityKo, DayofweekEntityKoSingle
from foxylib.tools.entity.entity_tool import Entity
from foxylib.tools.function.function_tool import FunctionTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from foxylib.tools.regex.regex_tool import RegexTool, rstr2wrapped, MatchTool
from foxylib.tools.span.span_tool import SpanTool
from foxylib.tools.string.string_tool import format_str, StringTool

class DayofweekSpanEntityKo:

    @classmethod
    def rstr_delim(cls):
        return '[-~]'

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=2))
    def pattern_delim(cls):
        return re.compile(RegexTool.rstr2rstr_words(cls.rstr_delim()), re.I)

    @classmethod
    @FunctionTool.wrapper2wraps_applied(lru_cache(maxsize=256))
    def str_span2is_gap(cls, str_in, span):
        return StringTool.str_span2is_blank_or_nullstr(str_in, span)

    @classmethod
    @f_iter2f_list
    def _str2entity_list_multiday(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls._str2entity_list_multiday, logging.DEBUG)
        entity_list_1day = DayofweekEntityKoSingle.str2entity_list(str_in)
        p_delim = cls.pattern_delim()
        m_list_delim = list(p_delim.finditer(str_in))
        span_ll = [
         lmap(Entity.j2span, entity_list_1day),
         lmap(MatchTool.match2span, m_list_delim),
         lmap(Entity.j2span, entity_list_1day)]
        f_span2is_gap = lambda span: cls.str_span2is_gap(str_in, span)
        j_tuple_list = list(SpanTool.spans_list_f_gap2j_tuples_valid(span_ll, f_span2is_gap))
        logger.debug({'j_tuple_list':j_tuple_list,  'entity_list_1day':entity_list_1day, 
         'm_list_delim':m_list_delim})
        for j_tuple in j_tuple_list:
            j1, j2, j3 = j_tuple
            entity_pair = (
             entity_list_1day[j1], entity_list_1day[j3])
            logger.debug({'j1':j1,  'j3':j3, 
             'entity_pair':entity_pair})
            span = Entity.j_pair2span(entity_pair)
            j_entity = {Entity.F.SPAN: span, 
             Entity.F.TEXT: StringTool.str_span2str(str_in, span), 
             Entity.F.VALUE: tmap(Entity.j2value, entity_pair)}
            yield j_entity

    @classmethod
    def _entity_1day2multiday(cls, j_entity_1day):
        v_1day = Entity.j2value(j_entity_1day)
        j_entity_multiday = merge_dicts([j_entity_1day,
         {Entity.F.VALUE: (v_1day,)}],
          vwrite=vwrite_overwrite)
        return j_entity_multiday

    @classmethod
    def str2entity_list(cls, str_in):
        logger = FoxylibLogger.func_level2logger(cls.str2entity_list, logging.DEBUG)
        entity_list_1day_raw = DayofweekEntityKo.str2entity_list(str_in)
        entity_list_multiday = cls._str2entity_list_multiday(str_in)
        span_list_multiday = lmap(Entity.j2span, entity_list_multiday)

        def entity_1day2is_not_covered(entity_1day):
            span_1day = Entity.j2span(entity_1day)
            for span_multiday in span_list_multiday:
                if SpanTool.covers(span_multiday, span_1day):
                    return False

            return True

        entity_list_1day_uncovered = lfilter(entity_1day2is_not_covered, entity_list_1day_raw)
        entity_list = lchain(lmap(cls._entity_1day2multiday, entity_list_1day_uncovered), entity_list_multiday)
        return entity_list