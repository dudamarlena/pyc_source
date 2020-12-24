# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/baron/baron/helpers.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 408 bytes
import json, sys
from os import linesep
from . import parse

def show(source_code):
    sys.stdout.write(json.dumps((parse(source_code)), indent=4) + linesep)


def show_file(target_file):
    with open(target_file, 'r') as (source_code):
        sys.stdout.write(json.dumps((parse(source_code.read())), indent=4) + linesep)


def show_node(node):
    sys.stdout.write(json.dumps(node, indent=4) + linesep)