# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/serial/json.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 1012 bytes
"""Handle JSON content."""
import json, re
from spynl.main.serial import objects
from spynl.main.serial.exceptions import MalformedRequestException

def loads(body, headers=None, context=None):
    """Return body as JSON."""
    try:
        decoder = objects.SpynlDecoder(context)
        return json.loads(body, object_hook=decoder)
    except ValueError as e:
        raise MalformedRequestException('application/json', str(e))


def dumps(body, pretty=False):
    """Return JSON body as string."""
    indent = None
    if pretty:
        indent = 4

    class JSONEncoder(json.JSONEncoder):

        def default(self, obj):
            return objects.encode(obj)

    return json.dumps(body, indent=indent, ensure_ascii=False, cls=JSONEncoder)


def sniff(body):
    """
    sniff to see if body is a json object.

    Body should start with any amount of whitespace and a {.
    """
    expression = re.compile('^\\s*\\{')
    return bool(re.match(expression, body))