# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/putzw/Documents/Projects/Source/jinjamator/jinjamator/plugins/content/json.py
# Compiled at: 2020-04-08 08:10:33
# Size of source mod 2**32: 713 bytes
from json import dumps as json_dumps

def dumps(data):
    """helper for jinja2"""
    return json_dumps(data, sort_keys=True, indent=2)