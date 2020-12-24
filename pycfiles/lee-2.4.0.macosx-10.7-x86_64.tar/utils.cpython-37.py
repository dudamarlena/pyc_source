# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zk/anaconda3/lib/python3.7/site-packages/lee/utils.py
# Compiled at: 2020-01-24 08:52:33
# Size of source mod 2**32: 303 bytes
import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

def jsonp(json_object):
    json_str = json.dumps(json_object, indent=4, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))