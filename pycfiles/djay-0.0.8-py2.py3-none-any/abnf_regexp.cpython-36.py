# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/abnf_regexp.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 9081 bytes
"""Module for the regular expressions crafted from ABNF."""
import sys
GEN_DELIMS = GENERIC_DELIMITERS = ':/?#[]@'
GENERIC_DELIMITERS_SET = set(GENERIC_DELIMITERS)
SUB_DELIMS = SUB_DELIMITERS = "!$&'()*+,;="
SUB_DELIMITERS_SET = set(SUB_DELIMITERS)
SUB_DELIMITERS_RE = "!$&'()\\*+,;="
RESERVED_CHARS_SET = GENERIC_DELIMITERS_SET.union(SUB_DELIMITERS_SET)
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
DIGIT = '0123456789'
UNRESERVED = UNRESERVED_CHARS = ALPHA + DIGIT + '._!-'
UNRESERVED_CHARS_SET = set(UNRESERVED_CHARS)
NON_PCT_ENCODED_SET = RESERVED_CHARS_SET.union(UNRESERVED_CHARS_SET)
UNRESERVED_RE = 'A-Za-z0-9._~\\-'
PERCENT_ENCODED = PCT_ENCODED = '%[A-Fa-f0-9]{2}'
PCHAR = '([' + UNRESERVED_RE + SUB_DELIMITERS_RE + ':@]|%s)' % PCT_ENCODED
SCHEME_RE = '[a-zA-Z][a-zA-Z0-9+.-]*'
_AUTHORITY_RE = '[^/?#]*'
_PATH_RE = '[^?#]*'
_QUERY_RE = '[^#]*'
_FRAGMENT_RE = '.*'
COMPONENT_PATTERN_DICT = {'scheme':SCHEME_RE, 
 'authority':_AUTHORITY_RE, 
 'path':_PATH_RE, 
 'query':_QUERY_RE, 
 'fragment':_FRAGMENT_RE}
URL_PARSING_RE = ('(?:(?P<scheme>{scheme}):)?(?://(?P<authority>{authority}))?(?P<path>{path})(?:\\?(?P<query>{query}))?(?:#(?P<fragment>{fragment}))?'.format)(**COMPONENT_PATTERN_DICT)
REGULAR_NAME_RE = REG_NAME = '((?:{0}|[{1}])*)'.format('%[0-9A-Fa-f]{2}', SUB_DELIMITERS_RE + UNRESERVED_RE)
IPv4_RE = '([0-9]{1,3}\\.){3}[0-9]{1,3}'
HEXDIG_RE = '[0-9A-Fa-f]{1,4}'
LS32_RE = '({hex}:{hex}|{ipv4})'.format(hex=HEXDIG_RE, ipv4=IPv4_RE)
_subs = {'hex':HEXDIG_RE, 
 'ls32':LS32_RE}
variations = [
 '(%(hex)s:){6}%(ls32)s' % _subs,
 '::(%(hex)s:){5}%(ls32)s' % _subs,
 '(%(hex)s)?::(%(hex)s:){4}%(ls32)s' % _subs,
 '((%(hex)s:)?%(hex)s)?::(%(hex)s:){3}%(ls32)s' % _subs,
 '((%(hex)s:){0,2}%(hex)s)?::(%(hex)s:){2}%(ls32)s' % _subs,
 '((%(hex)s:){0,3}%(hex)s)?::%(hex)s:%(ls32)s' % _subs,
 '((%(hex)s:){0,4}%(hex)s)?::%(ls32)s' % _subs,
 '((%(hex)s:){0,5}%(hex)s)?::%(hex)s' % _subs,
 '((%(hex)s:){0,6}%(hex)s)?::' % _subs]
IPv6_RE = ('(({0})|({1})|({2})|({3})|({4})|({5})|({6})|({7})|({8}))'.format)(*variations)
IPv_FUTURE_RE = 'v[0-9A-Fa-f]+\\.[%s]+' % (UNRESERVED_RE + SUB_DELIMITERS_RE + ':')
ZONE_ID = '(?:[' + UNRESERVED_RE + ']|' + PCT_ENCODED + ')+'
IPv6_ADDRZ_RFC4007_RE = IPv6_RE + '(?:(?:%25|%)' + ZONE_ID + ')?'
IPv6_ADDRZ_RE = IPv6_RE + '(?:%25' + ZONE_ID + ')?'
IP_LITERAL_RE = '\\[({0}|{1})\\]'.format(IPv6_ADDRZ_RFC4007_RE, IPv_FUTURE_RE)
HOST_RE = HOST_PATTERN = '({0}|{1}|{2})'.format(REG_NAME, IPv4_RE, IP_LITERAL_RE)
USERINFO_RE = '^([' + UNRESERVED_RE + SUB_DELIMITERS_RE + ':]|%s)+' % PCT_ENCODED
PORT_RE = '[0-9]{1,5}'
segments = {'segment':PCHAR + '*', 
 'segment-nz':PCHAR + '+', 
 'segment-nz-nc':PCHAR.replace(':', '') + '+'}
PATH_EMPTY = '^$'
PATH_ROOTLESS = '%(segment-nz)s(/%(segment)s)*' % segments
PATH_NOSCHEME = '%(segment-nz-nc)s(/%(segment)s)*' % segments
PATH_ABSOLUTE = '/(%s)?' % PATH_ROOTLESS
PATH_ABEMPTY = '(/%(segment)s)*' % segments
PATH_RE = '^(%s|%s|%s|%s|%s)$' % (
 PATH_ABEMPTY, PATH_ABSOLUTE, PATH_NOSCHEME, PATH_ROOTLESS, PATH_EMPTY)
FRAGMENT_RE = QUERY_RE = '^([/?:@' + UNRESERVED_RE + SUB_DELIMITERS_RE + ']|%s)*$' % PCT_ENCODED
RELATIVE_PART_RE = '(//%s%s|%s|%s|%s)' % (
 COMPONENT_PATTERN_DICT['authority'],
 PATH_ABEMPTY,
 PATH_ABSOLUTE,
 PATH_NOSCHEME,
 PATH_EMPTY)
HIER_PART_RE = '(//%s%s|%s|%s|%s)' % (
 COMPONENT_PATTERN_DICT['authority'],
 PATH_ABEMPTY,
 PATH_ABSOLUTE,
 PATH_ROOTLESS,
 PATH_EMPTY)
if sys.maxunicode > 65535:
    IPRIVATE = '\ue000-\uf8ff\U000f0000-\U000ffffd\U00100000-\U0010fffd'
    UCSCHAR_RE = '\xa0-\ud7ff豈-\ufdcfﷰ-\uffef𐀀-\U0001fffd𠀀-\U0002fffd\U00030000-\U0003fffd\U00040000-\U0004fffd\U00050000-\U0005fffd\U00060000-\U0006fffd\U00070000-\U0007fffd\U00080000-\U0008fffd\U00090000-\U0009fffd\U000a0000-\U000afffd\U000b0000-\U000bfffd\U000c0000-\U000cfffd\U000d0000-\U000dfffd\U000e1000-\U000efffd'
else:
    IPRIVATE = '\ue000-\uf8ff'
    UCSCHAR_RE = '\xa0-\ud7ff豈-\ufdcfﷰ-\uffef'
IUNRESERVED_RE = 'A-Za-z0-9\\._~\\-' + UCSCHAR_RE
IPCHAR = '([' + IUNRESERVED_RE + SUB_DELIMITERS_RE + ':@]|%s)' % PCT_ENCODED
isegments = {'isegment':IPCHAR + '*', 
 'isegment-nz':IPCHAR + '+', 
 'isegment-nz-nc':IPCHAR.replace(':', '') + '+'}
IPATH_ROOTLESS = '%(isegment-nz)s(/%(isegment)s)*' % isegments
IPATH_NOSCHEME = '%(isegment-nz-nc)s(/%(isegment)s)*' % isegments
IPATH_ABSOLUTE = '/(?:%s)?' % IPATH_ROOTLESS
IPATH_ABEMPTY = '(?:/%(isegment)s)*' % isegments
IPATH_RE = '^(?:%s|%s|%s|%s|%s)$' % (
 IPATH_ABEMPTY, IPATH_ABSOLUTE, IPATH_NOSCHEME, IPATH_ROOTLESS, PATH_EMPTY)
IREGULAR_NAME_RE = IREG_NAME = '(?:{0}|[{1}])*'.format('%[0-9A-Fa-f]{2}', SUB_DELIMITERS_RE + IUNRESERVED_RE)
IHOST_RE = IHOST_PATTERN = '({0}|{1}|{2})'.format(IREG_NAME, IPv4_RE, IP_LITERAL_RE)
IUSERINFO_RE = '^(?:[' + IUNRESERVED_RE + SUB_DELIMITERS_RE + ':]|%s)+' % PCT_ENCODED
IFRAGMENT_RE = '^(?:[/?:@' + IUNRESERVED_RE + SUB_DELIMITERS_RE + ']|%s)*$' % PCT_ENCODED
IQUERY_RE = '^(?:[/?:@' + IUNRESERVED_RE + SUB_DELIMITERS_RE + IPRIVATE + ']|%s)*$' % PCT_ENCODED
IRELATIVE_PART_RE = '(//%s%s|%s|%s|%s)' % (
 COMPONENT_PATTERN_DICT['authority'],
 IPATH_ABEMPTY,
 IPATH_ABSOLUTE,
 IPATH_NOSCHEME,
 PATH_EMPTY)
IHIER_PART_RE = '(//%s%s|%s|%s|%s)' % (
 COMPONENT_PATTERN_DICT['authority'],
 IPATH_ABEMPTY,
 IPATH_ABSOLUTE,
 IPATH_ROOTLESS,
 PATH_EMPTY)