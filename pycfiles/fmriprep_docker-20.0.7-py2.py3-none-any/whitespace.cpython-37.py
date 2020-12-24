# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/html5lib/filters/whitespace.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 1214 bytes
from __future__ import absolute_import, division, unicode_literals
import re
from . import base
from ..constants import rcdataElements, spaceCharacters
spaceCharacters = ''.join(spaceCharacters)
SPACES_REGEX = re.compile('[%s]+' % spaceCharacters)

class Filter(base.Filter):
    __doc__ = 'Collapses whitespace except in pre, textarea, and script elements'
    spacePreserveElements = frozenset(['pre', 'textarea'] + list(rcdataElements))

    def __iter__(self):
        preserve = 0
        for token in base.Filter.__iter__(self):
            type = token['type']
            if not type == 'StartTag' or preserve or token['name'] in self.spacePreserveElements:
                preserve += 1
            else:
                if type == 'EndTag' and preserve:
                    preserve -= 1
                else:
                    if (preserve or type) == 'SpaceCharacters' and token['data']:
                        token['data'] = ' '
                    else:
                        if not preserve:
                            if type == 'Characters':
                                token['data'] = collapse_spaces(token['data'])
            yield token


def collapse_spaces(text):
    return SPACES_REGEX.sub(' ', text)