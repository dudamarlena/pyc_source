# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\url_regex\url_regex.py
# Compiled at: 2019-07-29 08:20:44
# Size of source mod 2**32: 1914 bytes
import re
from . import tlds

class Url:

    def __init__(self, full: str, domain: str, protocol: str=None):
        self.full = full
        self.domain = domain
        self.protocol = protocol

    def __repr__(self):
        return '<Url full={0.full} domain={0.domain} protocol={0.protocol}'.format(self)


class UrlRegex:

    def __init__(self, input: str, strict: bool=True):
        self.strict = strict
        self.input = input
        buildReg = self.build_regex
        self.regex = buildReg
        self.links_found = {}

    @property
    def build_regex(self):
        tlds_sort = '|'.join([g for g in sorted(tlds.tlds_list)])
        protocol = f"(?:(?:[a-z]+:)?//){'?' if self.strict else ''}"
        auth = '(?:\\S+(?::\\S*)?@)?'
        host = '(?:(?:[a-z\\u00a1-\\uffff0-9][-_]*)*[a-z\\u00a1-\\uffff0-9]+)'
        domain = '(?:\\.(?:[a-z\\u00a1-\\uffff0-9]-*)*[a-z\\u00a1-\\uffff0-9]+)*'
        tld = '(?:\\.{})\\.?'.format('(?:[a-z\\u00a1-\\uffff]{2,})' if self.strict else f"(?:{tlds_sort})")
        port = '(?::\\d{2,5})?'
        path = '(?:[/?#][^\\s,."]*)?'
        regex = f"(?:({protocol}|www\\.)){auth}(?:(localhost|{host}{domain}{tld}))({port}{path})"
        return regex

    @property
    def detect(self):
        """ Checks if string includes one or more links """
        if re.search(self.regex, self.input.lower()):
            return True
        return False

    @property
    def links(self):
        """ Displays links in a pretty format """
        regex = re.findall(self.regex, self.input.lower())
        for i, g in enumerate(regex):
            self.links_found[i] = Url(f"{g[0]}{g[1]}{g[2]}", g[1], g[0] if g[0] else None)

        return list(self.links_found.values())