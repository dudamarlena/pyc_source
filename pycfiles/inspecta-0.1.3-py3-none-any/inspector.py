# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-inspecta/inspecta/inspector.py
# Compiled at: 2019-02-06 02:02:44
from __future__ import print_function
import rootpath
rootpath.append()
import re, pprint
from os import environ as env
from pygments import highlight, lexers, formatters
from termcolor import colored as color
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

DEFAULT_INSPECTOR_INDENT = 4
DEFAULT_INSPECTOR_DEPTH = None
DEFAULT_INSPECTOR_COLORS = True

def inspect(data, indent=None, depth=None, colors=False):
    if indent is None:
        indent = env.get('INSPECTOR_INDENT', None)
        indent = indent or env.get('INDENT', None)
        indent = indent or DEFAULT_INSPECTOR_INDENT
    if indent == False:
        indent = None
    if indent:
        if not isinstance(indent, int):
            indent = int(indent)
    if depth is None:
        depth = env.get('INSPECTOR_DEPTH', None)
        depth = depth or env.get('DEPTH', None)
        depth = depth or DEFAULT_INSPECTOR_DEPTH
    if depth == False:
        depth = None
    if depth:
        if not isinstance(depth, int):
            depth = int(depth)
    if colors is None:
        colors = env.get('INSPECTOR_COLORS', None)
        colors = colors or env.get('COLORS', None)
        colors = colors or DEFAULT_INSPECTOR_COLORS
    if colors == False:
        colors = None
    if colors:
        colors = bool(colors)
    colors = re.search('^true|1$', str(colors), flags=re.IGNORECASE)
    result = None
    try:
        if isinstance(data, dict):
            data = dict(data)
        result = pprint.pformat(data, indent=indent, depth=depth)
        if colors:
            lexer = lexers.PythonLexer()
            formatter = formatters.TerminalFormatter()
            result = highlight(result, lexer, formatter)
    except Exception as error:
        pass

    return result


def print(*args, **kwargs):
    return __builtin__.print(inspect(*args, **kwargs))