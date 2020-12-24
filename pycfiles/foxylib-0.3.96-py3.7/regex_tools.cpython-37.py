# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/regex/regex_tools.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 10699 bytes
from abc import ABC, abstractmethod
import re
from functools import lru_cache
from future.utils import lmap, lfilter
from nose.tools import assert_true
from foxylib.tools.collections.collections_tool import l_singleton2obj, lchain
from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.native.class_tools import cls2name
from foxylib.tools.native.object_tools import obj2cls
from foxylib.tools.span.span_tools import SpanToolkit, list_span2sublist
from foxylib.tools.string.string_tools import format_str

class RegexToolkit:

    @classmethod
    def rstr_list2or(cls, l_in):
        l_sorted = sorted(l_in, key=(lambda x: -len(x)))
        rstr_or = '|'.join(lmap(cls.rstr2wrapped, l_sorted))
        return rstr_or

    @classmethod
    def rstr2rstr_words_prefixed(cls, rstr, rstr_prefix_list=None):
        if not rstr_prefix_list:
            rstr_prefix_list = [
             '']
        l = [format_str('(?<=^{0})|(?<=\\s{0})|(?<=\\b{0})', rstr_prefix) for rstr_prefix in rstr_prefix_list]
        rstr_pre = cls.join('|', l)
        return format_str('{0}{1}', cls.rstr2wrapped(rstr_pre), cls.rstr2wrapped(rstr))

    @classmethod
    def rstr2rstr_words_suffixed(cls, rstr, rstr_suffix=None):
        rstr_suf = '(?=(?:{0})(?:\\s|\\b|$))'.format(rstr_suffix or '')
        return '(?:{0}){1}'.format(rstr, rstr_suf)

    @classmethod
    def rstr2rstr_words(cls, rstr, rstr_prefix_list=None, rstr_suffix=None):
        rstr_prefixed = cls.rstr2rstr_words_prefixed(rstr, rstr_prefix_list=rstr_prefix_list)
        rstr_words = cls.rstr2rstr_words_suffixed(rstr_prefixed, rstr_suffix=rstr_suffix)
        return rstr_words

    @classmethod
    def rstr2parenthesised(cls, s, rstr_pars=None):
        if rstr_pars is None:
            rstr_pars = ('\\(', '\\)')
        return format_str('{}{}{}', cls.rstr2wrapped(rstr_pars[0]), cls.rstr2wrapped(s), cls.rstr2wrapped(rstr_pars[1]))

    @classmethod
    def rstr2rstr_line_prefixed(cls, rstr, rstr_prefix=None):
        rstr_pre = '(?:(?<=^{0})|(?<=\\n{0}))'.format(rstr_prefix or '')
        return '{0}(?:{1})'.format(rstr_pre, rstr)

    @classmethod
    def rstr2rstr_line_suffixed(cls, rstr, rstr_suffix=None):
        rstr_suf = '(?=(?:{0})(?:\\n|$))'.format(rstr_suffix or '')
        return '(?:{}){}'.format(rstr, rstr_suf)

    @classmethod
    def rstr2rstr_line(cls, rstr, rstr_prefix=None, rstr_suffix=None):
        rstr_prefixed = cls.rstr2rstr_line_prefixed(rstr, rstr_prefix=rstr_prefix)
        rstr_line = cls.rstr2rstr_line_suffixed(rstr_prefixed, rstr_suffix=rstr_suffix)
        return rstr_line

    @classmethod
    def join(cls, delim, iterable):
        rstr_list_padded = map(lambda s: '(?:{0})'.format(s), iterable)
        return '(?:{0})'.format(delim.join(rstr_list_padded))

    @classmethod
    def name_rstr2named(cls, name, rstr):
        return format_str('(?P<{0}>{1})', name, rstr)

    @classmethod
    @lru_cache(maxsize=2)
    def pattern_blank(cls):
        return re.compile('\\s+')

    @classmethod
    def p_str2m_uniq(cls, pattern, s):
        m_list = list(pattern.finditer(s))
        if not m_list:
            return
        m = l_singleton2obj(m_list)
        return m

    @classmethod
    def rstr2rstr_last(cls, rstr):
        return '(?:{})(?!.*(?:{}))'.format(rstr)

    @classmethod
    def rstr2wrapped(cls, rstr):
        return '(?:{})'.format(rstr)


class MatchToolkit:

    @classmethod
    def i2m_right_before(cls, i, m_list):
        if not m_list:
            return
        else:
            m_list_valid = lfilter(lambda m: m.end() <= i, m_list)
            return m_list_valid or None
        m_max = max(m_list_valid, key=(lambda m: m.start()))
        return m_max

    @classmethod
    def match2se(cls, m):
        return cls.match2span(m)

    @classmethod
    def match2span(cls, m):
        return list(m.span())

    @classmethod
    def match_group2span(cls, m, groupname):
        return list(m.span(groupname))

    @classmethod
    def match2len(cls, m):
        return SpanToolkit.span2len(cls.match2span(m))

    @classmethod
    def match2start(cls, m):
        return cls.match2se(m)[0]

    @classmethod
    def match2end(cls, m):
        return cls.match2se(m)[1]

    @classmethod
    def match2text(cls, m):
        return m.group()

    @classmethod
    def match2str_group_list(cls, m):
        return [name for name, value in m.groupdict().items() if value is not None]

    @classmethod
    def match2str_group(cls, m):
        l = cls.match2str_group_list(m)
        return l_singleton2obj(l)

    @classmethod
    def match_group2str(cls, m, g):
        assert_true(g)
        if not m:
            return m
        return m.group(g)

    @classmethod
    def match2explode(cls, str_in, m):
        if not m:
            return str_in
        s, e = MatchToolkit.match2span(m)
        t = (str_in[:s], str_in[s:e], str_in[e:])
        return t

    @classmethod
    def match_list_limit2span_best(cls, m_list, len_limit, f_matches2score):
        if not m_list:
            return
        else:
            span_list_document = lmap(match2span, m_list)
            span_list_match = list(SpanToolkit.span_list_limit2span_of_span_longest_iter(span_list_document, len_limit))
            return span_list_match or None
        span_best_match = max(span_list_match, key=(lambda span_m: f_matches2score(list_span2sublist(m_list, span_m))))
        span_best_document = SpanToolkit.span_list_span2span_big(span_list_document, span_best_match)
        return span_best_document


class RegexNodeToolkit:

    class Type:
        FORMAT_NODE = 'format_node'
        RSTR_NODE = 'rstr_node'

    @classmethod
    def node_list2groupname(cls, node_list):
        logger = FoxylibLogger.func2logger(cls.node_list2groupname)
        name_list = lmap(cls2name, node_list)
        return '__'.join(name_list)

    @classmethod
    def _node_parents2name(cls, node, ancestors):
        l = lchain(ancestors, [node])
        return cls.node_list2groupname(l)

    @classmethod
    def _h_node2args_kwargs(cls, h, node):
        if not h:
            return ([], {})
        else:
            logger = FoxylibLogger.func2logger(cls._h_node2args_kwargs)
            args_kwargs = h.get(node)
            return args_kwargs or ([], {})
        return args_kwargs

    @classmethod
    def node2type(cls, node):
        return node.type()

    @classmethod
    def _node2rstr_unnamed(cls, node, ancestors, args=None, kwargs=None):
        logger = FoxylibLogger.func2logger(cls._node2rstr_unnamed)
        _args = args or []
        _kwargs = kwargs or {}
        if cls.node2type(node) == cls.Type.RSTR_NODE:
            rstr = (node.rstr)(*_args, **_kwargs)
            return rstr
        subnode_list = node.subnode_list()
        ancestors_and_me = lchain(ancestors, [node])
        rstr_list_subnode = [cls._node2rstr_named(sn, ancestors_and_me, args=args, kwargs=kwargs) for sn in subnode_list]
        str_format = (node.rformat)(*_args, **_kwargs)
        rstr = format_str(str_format, *rstr_list_subnode)
        return rstr

    @classmethod
    def _node2rstr_named(cls, node, ancestors, args=None, kwargs=None):
        logger = FoxylibLogger.func2logger(cls._node2rstr_named)
        rstr_unnamed = cls._node2rstr_unnamed(node, ancestors, args=args, kwargs=kwargs)
        rstr_named = RegexToolkit.name_rstr2named(cls._node_parents2name(node, ancestors), rstr_unnamed)
        return rstr_named

    @classmethod
    def node2rstr(cls, node, named=True, args=None, kwargs=None):
        logger = FoxylibLogger.func2logger(cls.node2rstr)
        if named:
            return cls._node2rstr_named(node, [], args=args, kwargs=kwargs)
        return cls._node2rstr_unnamed(node, [], args=args, kwargs=kwargs)

    @classmethod
    def node2pattern(cls, node, *_, **__):
        rstr = (cls.node2rstr)(node, *_, **__)
        return re.compile(rstr)

    @classmethod
    def match_nodes2groupname_list(cls, m, cls_node_list):
        str_group_list = MatchToolkit.match2str_group_list(m)
        nodename_list = lmap(cls2name, cls_node_list)
        str_group_list_related = lfilter(lambda s: s.split('__')[(-1)] in nodename_list, str_group_list)
        return str_group_list_related


match2start = MatchToolkit.match2start
match2end = MatchToolkit.match2end
match2span = MatchToolkit.match2span
match2text = MatchToolkit.match2text