# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/misc.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 4094 bytes
"""
Module containing compiled regular expressions and constants.

This module contains important constants, patterns, and compiled regular
expressions for parsing and validating URIs and their components.
"""
import re
from . import abnf_regexp
URI_COMPONENTS = [
 'scheme', 'authority', 'path', 'query', 'fragment']
important_characters = {'generic_delimiters':abnf_regexp.GENERIC_DELIMITERS, 
 'sub_delimiters':abnf_regexp.SUB_DELIMITERS, 
 're_sub_delimiters':abnf_regexp.SUB_DELIMITERS_RE, 
 'unreserved_chars':abnf_regexp.UNRESERVED_CHARS, 
 're_unreserved':abnf_regexp.UNRESERVED_RE}
GENERIC_DELIMITERS = abnf_regexp.GENERIC_DELIMITERS_SET
SUB_DELIMITERS = abnf_regexp.SUB_DELIMITERS_SET
RESERVED_CHARS = abnf_regexp.RESERVED_CHARS_SET
UNRESERVED_CHARS = abnf_regexp.UNRESERVED_CHARS_SET
NON_PCT_ENCODED = abnf_regexp.NON_PCT_ENCODED_SET
URI_MATCHER = re.compile(abnf_regexp.URL_PARSING_RE)
SUBAUTHORITY_MATCHER = re.compile('^(?:(?P<userinfo>{0})@)?(?P<host>{1}):?(?P<port>{2})?$'.format(abnf_regexp.USERINFO_RE, abnf_regexp.HOST_PATTERN, abnf_regexp.PORT_RE))
HOST_MATCHER = re.compile('^' + abnf_regexp.HOST_RE + '$')
IPv4_MATCHER = re.compile('^' + abnf_regexp.IPv4_RE + '$')
IPv6_MATCHER = re.compile('^\\[' + abnf_regexp.IPv6_ADDRZ_RFC4007_RE + '\\]$')
IPv6_NO_RFC4007_MATCHER = re.compile('^\\[%s\\]$' % abnf_regexp.IPv6_ADDRZ_RE)
PATH_MATCHER = re.compile(abnf_regexp.PATH_RE)
QUERY_MATCHER = re.compile(abnf_regexp.QUERY_RE)
FRAGMENT_MATCHER = QUERY_MATCHER
SCHEME_MATCHER = re.compile('^{0}$'.format(abnf_regexp.SCHEME_RE))
RELATIVE_REF_MATCHER = re.compile('^%s(\\?%s)?(#%s)?$' % (
 abnf_regexp.RELATIVE_PART_RE,
 abnf_regexp.QUERY_RE,
 abnf_regexp.FRAGMENT_RE))
ABSOLUTE_URI_MATCHER = re.compile('^%s:%s(\\?%s)?$' % (
 abnf_regexp.COMPONENT_PATTERN_DICT['scheme'],
 abnf_regexp.HIER_PART_RE,
 abnf_regexp.QUERY_RE[1:-1]))
IRI_MATCHER = re.compile(abnf_regexp.URL_PARSING_RE, re.UNICODE)
ISUBAUTHORITY_MATCHER = re.compile('^(?:(?P<userinfo>{0})@)?(?P<host>{1}):?(?P<port>{2})?$'.format(abnf_regexp.IUSERINFO_RE, abnf_regexp.IHOST_RE, abnf_regexp.PORT_RE), re.UNICODE)

def merge_paths(base_uri, relative_path):
    """Merge a base URI's path with a relative URI's path."""
    if base_uri.path is None:
        if base_uri.authority is not None:
            return '/' + relative_path
    path = base_uri.path or ''
    index = path.rfind('/')
    return path[:index] + '/' + relative_path


UseExisting = object()