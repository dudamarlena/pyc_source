# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/filters/whitespace.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
import re
from . import base
from ..constants import rcdataElements, spaceCharacters
spaceCharacters = (b'').join(spaceCharacters)
SPACES_REGEX = re.compile(b'[%s]+' % spaceCharacters)

class Filter(base.Filter):
    """Collapses whitespace except in pre, textarea, and script elements"""
    spacePreserveElements = frozenset([b'pre', b'textarea'] + list(rcdataElements))

    def __iter__(self):
        preserve = 0
        for token in base.Filter.__iter__(self):
            type = token[b'type']
            if type == b'StartTag' and (preserve or token[b'name'] in self.spacePreserveElements):
                preserve += 1
            elif type == b'EndTag' and preserve:
                preserve -= 1
            elif not preserve and type == b'SpaceCharacters' and token[b'data']:
                token[b'data'] = b' '
            elif not preserve and type == b'Characters':
                token[b'data'] = collapse_spaces(token[b'data'])
            yield token


def collapse_spaces(text):
    return SPACES_REGEX.sub(b' ', text)