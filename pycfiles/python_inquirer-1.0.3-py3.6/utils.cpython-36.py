# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/utils.py
# Compiled at: 2019-08-16 00:14:27
# Size of source mod 2**32: 930 bytes
from __future__ import print_function
import json, sys
from pprint import pprint
from pygments import highlight, lexers, formatters
__version__ = '0.1.2'
PY3 = sys.version_info[0] >= 3

def format_json(data):
    return json.dumps(data, sort_keys=True, indent=4)


def colorize_json(data):
    if PY3:
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
    else:
        if not isinstance(data, unicode):
            data = unicode(data, 'UTF-8')
    colorful_json = highlight(data, lexers.JsonLexer(), formatters.TerminalFormatter())
    return colorful_json


def print_json(data):
    pprint(colorize_json(format_json(data)))