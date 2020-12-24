# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/serial/py.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 320 bytes
"""function to dump python objects"""
from pprint import pprint
from io import StringIO

def dumps(body, pretty=False):
    """Return Python objects in body in text representation"""
    if pretty:
        stream = StringIO()
        pprint(body, stream=stream)
        return stream.getvalue()
    return repr(body)