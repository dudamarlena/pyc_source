# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/workspace/spynl-git/venv/src/spynl/spynl/main/serial/yaml.py
# Compiled at: 2017-01-16 09:58:52
# Size of source mod 2**32: 645 bytes
"""Handle YAML content"""
import re, yaml
from spynl.main.serial.exceptions import MalformedRequestException
expression = re.compile('^\\s*\\-')

def sniff(body):
    """Sniff body content, return True if YAML detected"""
    return bool(re.match(expression, body))


def dumps(body, pretty=False):
    """return YAML body as string"""
    if pretty:
        return yaml.dump(body, indent=4)
    else:
        return yaml.dump(body)


def loads(body, headers=None):
    """return body as YAML"""
    try:
        return yaml.load(body)
    except ValueError as e:
        raise MalformedRequestException('application/x-yaml', str(e))