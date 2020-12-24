# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/colorsrc.py
# Compiled at: 2017-01-24 10:14:25
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def get_hightlight_src(code, srcname, linenos=False, stripall=True):
    try:
        lexer = get_lexer_by_name(srcname, stripall=stripall)
    except:
        return code

    formatter = HtmlFormatter(linenos=linenos, cssclass='source')
    result = highlight(code, lexer, formatter)
    return result