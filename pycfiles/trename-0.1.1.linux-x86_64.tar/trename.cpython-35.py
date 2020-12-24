# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/trename/trename.py
# Compiled at: 2017-05-04 10:57:09
# Size of source mod 2**32: 978 bytes
import re

class NoMatchException(Exception):
    pass


class IdentifiersNotFound(Exception):

    def __init__(self, identifiers=None):
        self.identifiers = identifiers


def get_identifiers(pattern_string):
    m = re.findall('\\{(\\w+)\\}', pattern_string)
    if not m:
        return []
    return m


def validate_patterns(pattern_in, pattern_out):
    ids_in = set(get_identifiers(pattern_in))
    ids_out = set(get_identifiers(pattern_out))
    ids_not_found = [s for s in ids_out if s not in ids_in]
    if ids_not_found:
        raise IdentifiersNotFound(ids_not_found)


def to_re_in(tpl):
    return '^' + re.sub('\\{(\\w+)\\}', '(?P<\\1>.+)', tpl) + '$'


def to_re_out(tpl):
    return re.sub('\\{(\\w+)\\}', '\\\\g<\\1>', tpl)


def new_name(filename, tpl_in, tpl_out):
    re_in = to_re_in(tpl_in.replace('.', '\\.'))
    re_out = to_re_out(tpl_out)
    if not re.match(re_in, filename):
        raise NoMatchException()
    return re.sub(re_in, re_out, filename)