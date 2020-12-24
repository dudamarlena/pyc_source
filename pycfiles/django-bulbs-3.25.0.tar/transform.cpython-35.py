# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/instant_articles/transform.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 281 bytes
from .parser import parse_body

def transform(html, renderer):
    """Convert blob of body content HTML into another output format (ex: FB Instant Article).
    This wires up separate "parser" and "renderer" subsystems.
    """
    return renderer.generate_body(parse_body(html))