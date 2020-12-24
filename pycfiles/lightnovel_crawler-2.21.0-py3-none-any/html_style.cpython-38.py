# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\assets\html_style.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 1756 bytes
import re
from pathlib import Path
ROOT = Path(__file__).parent
with open(str(ROOT / 'html_style.css'), 'r') as (f):
    style = f.read()

def get_value():
    return _minify(style)


def _minify(css):
    result = ''
    css = re.sub('/\\*[\\s\\S]*?\\*/', '', css)
    css = re.sub('\\s+', ' ', css)
    css = re.sub('#([0-9a-f])\\1([0-9a-f])\\2([0-9a-f])\\3(\\s|;)', '#\\1\\2\\3\\4', css)
    css = re.sub(':\\s*0(\\.\\d+([cm]m|e[mx]|in|p[ctx]))\\s*;', ':\\1;', css)
    for rule in re.findall('([^{]+){([^}]*)}', css):
        selectors = [re.sub('(?<=[\\[\\(>+=])\\s+|\\s+(?=[=~^$*|>+\\]\\)])', '', selector.strip()) for selector in rule[0].split(',')]
        properties = {}
        porder = []
        for prop in re.findall('(.*?):(.*?)(;|$)', rule[1]):
            key = prop[0].strip().lower()
            if key not in porder:
                porder.append(key)
            properties[key] = prop[1].strip()
            if properties:
                result += '%s{%s}' % (','.join(selectors),
                 ''.join(['%s:%s;' % (key, properties[key]) for key in porder])[:-1])
        else:
            return result