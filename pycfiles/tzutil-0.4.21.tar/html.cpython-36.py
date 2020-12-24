# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/txt/html.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 1768 bytes
import re
from tzutil.unescape import unescape
from html import escape

def txt2html(txt):
    if not txt:
        return ''
    else:
        r = []
        for i in txt.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
            if i.strip():
                r.append(escape(i))

        return '<p>' + '</p><p>'.join(r) + '</p>'


def html2txt_brief(data):
    data = data.replace('</p>', '\n').replace('<br>', '\n').replace('</div>', '\n')
    p = re.compile('<.*?>')
    return unescape(p.sub('', data)).strip()


def cnenlen(s):
    return len(s.encode('gb18030', 'ignore')) // 2


def cnencut(s, length):
    s = s.encode('gb18030', 'ignore')[:length * 2].decode('gb18030', 'ignore')
    return s


def cnenoverflow(s, length):
    txt = cnencut(s, length)
    if txt != s:
        txt = '%s … …' % txt.rstrip()
        has_more = True
    else:
        has_more = False
    return (
     txt, has_more)


def txt_rstrip(txt):
    return '\n'.join(map(str.rstrip, txt.replace('\r\n', '\n').replace('\r', '\n').rstrip('\n ').split('\n')))


RE_NUMBER_STR = '[-+]? (?: (?: \\d* \\. \\d+ ) | (?: \\d+ \\.? ) )(?: [Ee] [+-]? \\d+ ) ?'
RE_NUMBER = re.compile(RE_NUMBER_STR, re.VERBOSE)

def remove_number(txt):
    return RE_NUMBER.sub('-', txt)


if __name__ == '__main__':
    print(remove_number('啊3'))
    txt = '；，（）。'
    print(txt)
    print(全角转半角(txt))