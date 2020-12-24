# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/core/blacklist.py
# Compiled at: 2019-05-16 13:41:33
import re
_FILE_FILTERS = set()
_COMMAND_FILTERS = set()
_PATTERN_FILTERS = set()
_KEYWORD_FILTERS = set()

def add_file(f):
    _FILE_FILTERS.add(re.compile(f))


def add_command(f):
    _COMMAND_FILTERS.add(re.compile(f))


def add_pattern(f):
    _PATTERN_FILTERS.add(f)


def add_keyword(f):
    _KEYWORD_FILTERS.add(f)


def allow_file(c):
    return not any(f.match(c) for f in _FILE_FILTERS)


def allow_command(c):
    return not any(f.match(c) for f in _COMMAND_FILTERS)


def get_disallowed_patterns():
    return _PATTERN_FILTERS


def get_disallowed_keywords():
    return _KEYWORD_FILTERS