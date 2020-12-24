# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vtwt/util.py
# Compiled at: 2010-06-23 10:55:00
import re
from htmlentitydefs import name2codepoint
from twisted.python.text import greedyWrap
from twisted.web.error import Error as WebError
_HTMLENT_CODEPOINT_RE = re.compile(('&({0}|#\\d+);').format(('|').join(name2codepoint.keys())))

def recodeText(text):
    """Parses things like &amp; and &#8020; into real characters."""

    def _entToUnichr(match):
        ent = match.group(1)
        try:
            if ent.startswith('#'):
                char = unichr(int(ent[1:]))
            else:
                char = unichr(name2codepoint[ent])
        except:
            char = match.group(0)

        return char

    return _HTMLENT_CODEPOINT_RE.sub(_entToUnichr, text)


def failWhale(error, columns=80):
    if isinstance(error, WebError):
        emsg = ('{0.status} {0.message}').format(error)
    else:
        emsg = str(error)
    return whale(emsg, columns)


_whaleFmt = '   _{lines}__\n|\\/{space} x \\\n}}   {body}   |\n|/\\{lines}__-/'
_whalePaddingLen = 6

def whale(msg, columns=80):
    width = columns - _whalePaddingLen
    lines = []
    for line in msg.splitlines():
        lines.extend(greedyWrap(line, width))

    lineLength = max(map(len, lines))
    msg = ('{0}|\n|{0}').format(_whalePaddingLen / 2 * ' ').join(map(lambda l: ('{0:{1}}').format(l, lineLength), lines))
    return _whaleFmt.format(space=' ' * lineLength, lines='_' * lineLength, length=lineLength, body=msg)