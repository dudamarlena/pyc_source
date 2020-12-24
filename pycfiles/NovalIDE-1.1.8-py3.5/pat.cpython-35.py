# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/syntax/pat.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1224 bytes
import re

def matches_any(name, alternates):
    """Return a named group pattern matching list of alternates."""
    return '(?P<%s>' % name + '|'.join(alternates) + ')'


def get_keyword_pat(kwlist):
    """
        匹配关键字
    """
    kw = '\\b' + matches_any('keyword', kwlist) + '\\b'
    return kw


def get_builtin_pat(builtinlist):
    """
        匹配内建函数
    """
    builtin = '([^.\'\\"\\\\#]\\b|^)' + matches_any('builtin', builtinlist) + '\\b'
    return builtin


def get_number_pat():
    """
        匹配数字
    """
    number = matches_any('number', ['\\b(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?'])
    return number


stringprefix = '(\\br|u|ur|R|U|UR|Ur|uR|b|B|br|Br|bR|BR)?'

def get_sqstring_pat():
    """
        匹配单引号字符串
    """
    sqstring = stringprefix + "'[^'\\\\\\n]*(\\\\.[^'\\\\\\n]*)*'?"
    return sqstring


def get_dqstring_pat():
    """
        匹配双引号字符串
    """
    dqstring = stringprefix + '"[^"\\\\\\n]*(\\\\.[^"\\\\\\n]*)*"?'
    return dqstring


def get_prog(pat):
    prog = re.compile(pat, re.S)
    return prog


def get_id_prog():
    """
        匹配标识符
    """
    idprog = re.compile('\\s+(\\w+)', re.S)
    return idprog