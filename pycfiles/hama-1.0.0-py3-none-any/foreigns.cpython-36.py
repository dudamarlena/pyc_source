# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/foreigns.py
# Compiled at: 2020-04-23 12:01:32
# Size of source mod 2**32: 324 bytes
from .tagging import tag

def foreigns():
    """Extract foreign words from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as foreign words.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'f']
    return filtered