# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/envoy_data_plane/envoy/type/matcher.py
# Compiled at: 2020-01-30 00:14:53
# Size of source mod 2**32: 3229 bytes
from dataclasses import dataclass
from typing import List, Optional
import betterproto

@dataclass
class RegexMatcher(betterproto.Message):
    __doc__ = 'A regex matcher designed for safety when used with untrusted input.'
    google_re2 = betterproto.message_field(1,
      group='engine_type')
    google_re2: 'RegexMatcherGoogleRE2'
    regex = betterproto.string_field(2)
    regex: str


@dataclass
class RegexMatcherGoogleRE2(betterproto.Message):
    __doc__ = "\n    Google's `RE2 <https://github.com/google/re2>`_ regex engine. The regex\n    string must adhere to the documented `syntax\n    <https://github.com/google/re2/wiki/Syntax>`_. The engine is designed to\n    complete execution in linear time as well as limit the amount of memory\n    used.\n    "
    max_program_size = betterproto.message_field(1,
      wraps=(betterproto.TYPE_UINT32))
    max_program_size: Optional[int]


@dataclass
class StringMatcher(betterproto.Message):
    __doc__ = 'Specifies the way to match a string. [#next-free-field: 6]'
    exact = betterproto.string_field(1, group='match_pattern')
    exact: str
    prefix = betterproto.string_field(2, group='match_pattern')
    prefix: str
    suffix = betterproto.string_field(3, group='match_pattern')
    suffix: str
    regex = betterproto.string_field(4, group='match_pattern')
    regex: str
    safe_regex = betterproto.message_field(5, group='match_pattern')
    safe_regex: 'RegexMatcher'


@dataclass
class ListStringMatcher(betterproto.Message):
    __doc__ = 'Specifies a list of ways to match a string.'
    patterns = betterproto.message_field(1)
    patterns: List['StringMatcher']