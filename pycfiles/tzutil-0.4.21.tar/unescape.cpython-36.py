# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/unescape.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 1339 bytes
import html.entities, re
from urllib.parse import urlparse
BLOD_LINE = re.compile('^\\s*\\*\\*[\\r\\n]+', re.M)
_char = re.compile('&(\\w+?);')
_dec = re.compile('&#(\\d{2,4});')
_hex = re.compile('&#x(\\d{2,4});')

def _char_unescape(m, defs=html.entities.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)


import re, html.entities

def unescape(s):

    def entity2char(m):
        entity = m.group(1)
        if entity in html.entities.name2codepoint:
            return chr(html.entities.name2codepoint[entity])
        else:
            return ' '

    t = re.sub('&(%s);' % '|'.join(html.entities.name2codepoint), entity2char, s)
    t = re.sub('&#(\\d+);', lambda x: chr(int(x.group(1))), t)
    return re.sub('&#x(\\w+);', lambda x: chr(int(x.group(1), 16)), t)


if __name__ == '__main__':
    print(unescape("<option value='&#20013;&#22269;&#35821;&#35328;&#25991;&#23398;&#31995;'>&#20013;&#22269;&#35821;&#35328;&#25991;&#23398;&#31995;</option>"))